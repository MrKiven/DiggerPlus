# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages

def _get_version():
    v_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'diggerplus', '__init__.py')
    ver_info_str = re.compile(r".*version_info = \((.*?)\)", re.S). \
        match(open(v_file_path).read()).group(1)
    return re.sub(r'(\'|"|\s+)', '', ver_info_str).replace(',', '.')


entry_points = {
    "console_scripts": ["diggerplus=diggerplus.bin.cmds:diggerplus"]
}


install_requires = []
tests_requires = []

with open('requirements.txt') as f:
    for r in f:
        install_requires.append(r)

with open('dev_requirements.txt') as f:
    for r in f:
        tests_requires.append(r)

setup(
    name='diggerplus',
    version=_get_version(),
    long_description=open('README.md').read(),
    author="DiggerPlus",
    author_email="diggerplus@163.com",
    packages=find_packages(),
    package_data={"": ["LICENSE"]},
    url="http://www.diggerplus.org/",
    entry_points=entry_points,
    tests_require=tests_requires,
    install_requires=install_requires,
)
