# -*- coding: utf-8 -*-

import pytest

from diggerplus import __version__ as version


@pytest.fixture
def diggerplus_version():
    return version
