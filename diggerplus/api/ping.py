# -*- coding: utf-8 -*-

import logging

from flask import Blueprint

from diggerplus import __version__
from .base import status_OK, MethodView


logger = logging.getLogger(__name__)

bp = Blueprint('ping', __name__, url_prefix='/api')


class Ping(MethodView):
    blueprint = bp
    url_rules = ['/ping']
    logger = logger

    def get(self):
        return status_OK({'version': __version__})
