# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, request

from .base import status_OK, status_Created, status_ResetContent, MethodView
from ..models.todo import TODOModel
from ..exc import NotFoundException, ExistedException
from ..consts import ALREADY_EXISTS_MESSSAGE

logger = logging.getLogger(__name__)


bp = Blueprint('todos', __name__, url_prefix='/api')


class TODOS(MethodView):
    blueprint = bp
    url_rule = '/todos/<title>'
    logger = logger

    def get(self, title):
        todo = TODOModel.get_by_title(title)
        if todo:
            return status_OK(todo.to_dict())
        raise NotFoundException("TODO: {!r} not found!".format(title))

    def post(self, title):
        todo = TODOModel.get_by_title(title)
        if todo:
            raise ExistedException(
                ALREADY_EXISTS_MESSSAGE.format(self.__class__.__name__, title))
        TODOModel.add(title=title)
        return status_Created()

    def put(self, title):
        data = request.get_json(force=True, silent=True)
        if data is None:
            data = request.values.to_dict()
        todo = TODOModel.get_by_title(title)
        if todo:
            todo.update(**data)
            return status_ResetContent()
        raise NotFoundException("TODO: {!r} not found!".format(title))
