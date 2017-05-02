# -*- coding: utf-8 -*-

from flask import Flask

from diggerplus.api import register_all_bps


class DiggerPlus(Flask):

    def __init__(self, *args, **kwargs):
        super(DiggerPlus, self).__init__(*args, **kwargs)
        self.register_blueprints()

    def register_blueprints(self):
        register_all_bps(self)


app = DiggerPlus(__name__)
