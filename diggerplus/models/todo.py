# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    Integer,
    String,
    SmallInteger
)

from .base import ModelBase, DBSession


class TODOModel(ModelBase):

    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, default="")
    is_done = Column(SmallInteger, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_done': self.is_done
        }

    @classmethod
    def get(cls, todo_id):
        session = DBSession()
        todo = session.query(cls).get(todo_id)
        if todo:
            return todo.to_dict()

    @classmethod
    def add(cls, title):
        session = DBSession()
        session.add(cls)
        session.commit()
