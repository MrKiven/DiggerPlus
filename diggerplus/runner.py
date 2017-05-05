# -*- coding: utf-8 -*-

import gunicorn.util
from gunicorn.app.wsgiapp import WSGIApplication


class DiggerPlusApp(WSGIApplication):

    def init(self, parser, opts, args):
        super(DiggerPlusApp, self).init(parser, opts, args)
        self.app_uri = "diggerplus.app:app"

    def load_wsgiapp(self):
        from .wsgi import WSGIMiddleware
        self.chdir()
        app = gunicorn.util.import_app(self.app_uri)
        return WSGIMiddleware(app)


def start():
    DiggerPlusApp().run()
