# -*- coding: utf-8 -*-

import time

from . import signals


class WSGIMiddleware(object):
    """Middleware class for WSGI app."""

    def __init__(self, app):
        self.app = app
        self.signal = signals.wsgi_signal_wrapper

    def __call__(self, environ, start_response):
        ctx = signals.APICallSignalContext()
        ctx.start_at = time.time()
        try:
            return self.app(environ, start_response)
        except Exception as exc:
            ctx.end_at = time.time()
            ctx.exc = exc
            self.signal.called_exc.send(ctx)
            raise
        finally:
            ctx.end_at = time.time()
            self.signal.called.send(ctx)
