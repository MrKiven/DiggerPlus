# -*- coding: utf-8 -*-

from diggerplus.db import mode_base, db_manager


ModelBase = mode_base()
DBSession = db_manager.get_session('diggerplus')
