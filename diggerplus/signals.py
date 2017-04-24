# -*- coding: utf-8 -*-

from blinker import Namespace

signal = Namespace().signal


class SignalContext(object):
    """Context object to hold data pass through."""


class APICallSignalContext(SignalContext):

    @property
    def cost(self):
        return 1000 * (self.end_at - self.start_at)


class SignalWSGIWrapper(object):

    def __init__(self):
        self.called = signal("after_request_called")
        self.called_exc = signal("after_request_called_exc")


wsgi_signal_wrapper = SignalWSGIWrapper()


def register_receivers():
    """Should register before load app"""
    wsgi_signal_wrapper.called.connect(on_single_called)
    wsgi_signal_wrapper.called_exc.connect(on_single_called_exc)


def on_single_called(ctx):
    pass


def on_single_called_exc(ctx):
    pass
