# -*- coding: utf-8 -*-

import click


@click.group()
@click.version_options()
def diggerplus():
    """DiggerPlus cmds entry point"""
