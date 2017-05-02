# -*- coding: utf-8 -*-

import logging

from flask import Blueprint

from .base import status_OK, MethodView
from ..models.todo import TODOModel
from ..exc import NotFoundException
from ..consts import NOT_FOUND_MESSAGE

logger = logging.getLogger(__name__)


bp = Blueprint('todos', __name__, url_prefix='/api')


class TODOS(MethodView):
    blueprint = bp
    url_rule = '/todo/<int:id>'
    logger = logger

    def get(self, id):
        todo = TODOModel.get(id)
        if todo:
            return status_OK(todo.to_dict())
        raise NotFoundException(
            NOT_FOUND_MESSAGE.format(self.__class__.__name__, id))
