# -*- coding: utf-8 -*-

from flask import current_app
from flask import json
from flask.views import MethodView


def status(code):
    def response(*args, **kwargs):
        if args and kwargs:
            raise TypeError("Cannot pass both args and kwargs.")
        elif len(args) == 1:
            data = args[0]
        else:
            data = args or kwargs

        if data:
            data = (json.dumps(data), '\n')
        else:
            data = None

        return current_app.response_class(
            response=data,
            status=code,
            mimetype=current_app.config['JSONIFY_MIMETYPE']
        )
    return response

status_OK = status(200)
status_Created = status(201)
status_NoContent = status(204)
status_ResetContent = status(205)


class DPMethodView(MethodView):

    @classmethod
    def register(cls):
        bp = getattr(cls, 'blueprint', None)
        url_rule = getattr(cls, 'url_rule', '')
        if not bp:
            bp = getattr(cls, 'app', None)
            raise RuntimeError(
                "Need blueprint or app instance in %r" % cls.__name__)
        bp.add_url_rule(url_rule, view_func=cls.as_view(cls.__name__))
