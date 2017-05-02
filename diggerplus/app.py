# -*- coding: utf-8 -*-

from flask import Flask, jsonify

from diggerplus.api import register_all_bps
from diggerplus.exc import NotFoundException


class DiggerPlus(Flask):

    def __init__(self, *args, **kwargs):
        super(DiggerPlus, self).__init__(*args, **kwargs)
        self.register_blueprints()
        self.register_error_handlers()

    def register_blueprints(self):
        register_all_bps(self)

    def register_error_handlers(self):
        self.register_error_handler(NotFoundException, self.not_found)

    @staticmethod
    def not_found(err):
        res = jsonify(err.to_dict())
        res.status_code = err.status_code
        return res


app = DiggerPlus(__name__)
