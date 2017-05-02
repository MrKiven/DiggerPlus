# -*- coding: utf-8 -*-


class BaseDiggerPlusException(Exception):
    """Api exception handler class"""
    status_code = 500

    def __init__(self, msg, status_code=None, payload=None):
        super(BaseDiggerPlusException, self).__init__(msg)
        self.msg = msg
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.msg
        rv['status_code'] = self.status_code
        return rv


class DiggerPlusException(BaseDiggerPlusException):
    status_code = 501


class NotFoundException(DiggerPlusException):
    status_code = 404
