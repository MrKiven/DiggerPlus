# -*- coding: utf-8 -*-

import os
import pkgutil
import importlib


def load_module_attrs(attr_name, pkg_path, package, prefix='.'):
    attrs = []

    for _, name, ispkg in pkgutil.iter_modules([pkg_path]):
        module = importlib.import_module(prefix + name, package)
        attr = getattr(module, attr_name, None)
        if attr:
            attrs.append(attr)

        if ispkg:
            next_pkg_path = os.path.join(pkg_path, name)
            next_prefix = prefix + name + '.'
            pkg_attrs = load_module_attrs(attr_name, next_pkg_path, package,
                                          next_prefix)
            attrs.append(pkg_attrs)

    return attrs
