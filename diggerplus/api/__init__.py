# -*- coding: utf-8 -*-


"""
  DiggerPlus Api Modules
  ~~~~~~~~~~~~~~~~~~~~~~

  All api for diggerplus backend.
"""

from . import ping


def register_all_views():
    ping.Ping.register()


def register_all_bps(app):
    app.register_blueprint(ping.bp)
