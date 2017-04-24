# -*- coding: utf-8 -*-


"""
  DiggerPlus Api Modules
  ~~~~~~~~~~~~~~~~~~~~~~

  All api for diggerplus backend.
"""

from flask import current_app
from flask import json


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
