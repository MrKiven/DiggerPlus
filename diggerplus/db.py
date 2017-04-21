# -*- coding: utf-8 -*-

import random
import uuid
import logging

import settings

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

logger = logging.getLogger(__name__)


class RoutingSession(Session):
    pass


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
            info=info or {"name": uuid.uuid4().hex}))
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
        return make_session(engines, info={"name", db})

    def close_session(self, should_close_connection=False):
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
