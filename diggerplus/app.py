# -*- coding: utf-8 -*-

from flask import Flask

from .api.ping import bp as ping_bp

app = Flask(__name__)
app.register_blueprint(ping_bp)
