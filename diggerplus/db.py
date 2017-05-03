# -*- coding: utf-8 -*-

import random
import uuid
import logging

import settings

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class RoutingSession(Session):
    _name = None

    def __init__(self, engines, *args, **kwargs):
        super(RoutingSession, self).__init__(*args, **kwargs)
        self.engines = engines
        self.slave_engines = [e for role, e in engines.items()
                              if role != 'master']
        if not self.slave_engines:
            self.slave_engines = engines

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """contextmanager

            with DBSession() as session:
                session.add(instance)

        """
        try:
            if exc_val is None:
                self.flush()
                self.commit()
            elif isinstance(exc_val, SQLAlchemyError):
                self.rollback()
        except SQLAlchemyError:
            self.rollback()
            raise
        finally:
            self.close()

    def get_bind(self, mapper=None, clause=None):
        if self._name:
            return self.engines[self._name]
        elif self._flushing:
            return self.engines['master']
        else:
            return random.choice(self.slave_engines)

    def using_bind(self, name):
        self._name = name
        return self


def patch_engine(engine):
    pool = engine.pool
    pool._origin_recycle = pool._recycle
    del pool._recycle
    setattr(pool.__class__, '_recycle', RecycleField())
    return engine


def make_session(engines, info=None):
    session = scoped_session(
        sessionmaker(
            class_=RoutingSession,
            expire_on_commit=False,
            engines=engines,
            info=info or {"name": uuid.uuid4().hex})
    )
    return session


def close_connections(engines, transactions):
    if engines and transactions:
        for engine in engines:
            for parent in transactions:
                conn = parent._connections.get(engine)
                if conn:
                    conn = conn[0]
                    conn.invalidate()


class RecycleField(object):

    def __get__(self, instance, kclass):
        if instance is not None:
            return int(random.uniform(0.75, 1) * instance._origin_recycle)
        raise AttributeError


class ModelMeta(DeclarativeMeta):
    def __new__(self, name, bases, attrs):
        cls = DeclarativeMeta.__new__(self, name, bases, attrs)

        # TODO: Here to add hooks
        return cls


def mode_base():
    return declarative_base(metaclass=ModelMeta)


class DBManager(object):
    def __init__(self):
        self.session_map = {}

    def create_session(self):
        if not settings.DB_SETTINGS:
            raise ValueError("DB SETTINGS is empty, check it.")
        for db, db_settings in settings.DB_SETTINGS.iteritems():
            self.add_session(db, db_settings)

    def add_session(self, name, config):
        if name in self.session_map:
            raise ValueError("Duplicate session name {}, "
                             "please check your config".format(name))
        session = self._make_session(name, config)
        self.session_map[name] = session
        return session

    def get_session(self, name):
        try:
            return self.session_map[name]
        except KeyError:
            raise KeyError(
                "`%s` session not created, check `DB_SETTINGS`" % name)

    @classmethod
    def _make_session(cls, db, config):
        urls = config['urls']
        for name, url in urls.iteritems():
            assert url, "Url configured not property for %s:%s" % (db, url)
        pool_size = config.get("pool_size", settings.DEFAULT_DB_POOL_SIZE)
        max_overflow = config.get(
            "max_overflow", settings.DEFAULT_MAX_OVERFLOW)
        pool_recycle = config.get(
            "pool_recycle", settings.DEFAULT_POOL_RECYCLE)
        engines = {
            role: cls.create_engine(dsn,
                                    pool_size=pool_size,
                                    max_overflow=max_overflow,
                                    pool_recycle=pool_recycle,
                                    execution_options={'role': role})
            for role, dsn in urls.iteritems()
        }
        return make_session(engines, info={"name": db})

    def close_sessions(self, should_close_connection=False):
        dbsessions = self.session_map
        for dbsession in dbsessions.itervalues():
            if should_close_connection:
                session = dbsession()
                if session.transaction is not None:
                    close_connections(session.engines.itervalues(),
                                      session.transaction._iterate_parents())
            try:
                dbsession.remove()
            except:
                logger.exception("Error closing session")

    @classmethod
    def create_engine(cls, *args, **kwargs):
        engine = patch_engine(sqlalchemy_create_engine(*args, **kwargs))
        return engine


db_manager = DBManager()
db_manager.create_session()
