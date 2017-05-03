# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    String,
    SmallInteger
)

from .base import Model


class TODOModel(Model):

    __tablename__ = 'todo'

    title = Column(String, default="")
    is_done = Column(SmallInteger, default=0)

    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter(cls.title==title).first()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_done': self.is_done
        }
