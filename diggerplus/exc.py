# -*- coding: utf-8 -*-


class DiggerPlusException(Exception):
    """Api exception handler class"""
    status_code = 500

    def __init__(self, msg, status_code=None, payload=None):
        super(DiggerPlusException, self).__init__()
        self.msg = msg
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.msg
        rv['status_code'] = self.status_code
        return rv


class NotFoundException(DiggerPlusException):
    status_code = 404
