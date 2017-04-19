# -*- coding: utf-8 -*-

import click


@click.group()
@click.version_option()
def diggerplus():
    """DiggerPlus commands entry point"""
