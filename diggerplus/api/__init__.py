# -*- coding: utf-8 -*-


"""
  DiggerPlus Api Modules
  ~~~~~~~~~~~~~~~~~~~~~~

  All api for diggerplus backend.
"""

import os

from diggerplus.utils import load_module_attrs

_current_path = os.path.dirname(os.path.abspath(__file__))


def register_all_bps(app, _pkg=__name__):
    bps = load_module_attrs('bp', _current_path, _pkg)
    [app.register_blueprint(bp) for bp in bps]
