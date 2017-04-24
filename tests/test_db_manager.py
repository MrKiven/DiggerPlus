# -*- coding: utf-8 -*-

from __future__ import absolute_import


from diggerplus.settings import DB_SETTINGS
from diggerplus.db import db_manager


def test_auto_create_session():
    assert db_manager.session_map
    for session_name in DB_SETTINGS:
        assert session_name in db_manager.session_map
