# -*- coding: utf-8 -*-

from flask import Blueprint

from diggerplus import __version__
from .base import status_OK, DPMethodView

bp = Blueprint('ping', __name__, url_prefix='/api')


class Ping(DPMethodView):
    blueprint = bp
    url_rule = '/ping'
    methods = ['GET']

    def get(self):
        return status_OK({'version': __version__})
