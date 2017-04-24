# -*- coding: utf-8 -*-

import click


@click.group()
@click.version_option()
def diggerplus():
    """DiggerPlus commands entry point"""


@diggerplus.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True
    },
    add_help_option=False)
def start():
    from diggerplus.runner import start
    start()
