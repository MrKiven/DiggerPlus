# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.views import MethodView

from diggerplus import __version__
from . import status_OK

bp = Blueprint('ping', __name__, url_prefix='/api')


class Ping(MethodView):

    methods = ['GET']

    def get(self):
        return status_OK({'version': __version__})

bp.add_url_rule('/ping', view_func=Ping.as_view(Ping.__name__))
