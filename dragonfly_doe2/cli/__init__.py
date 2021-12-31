"""dragonfly-doe2 commands which will be added to dragonfly command line interface."""
import click
from dragonfly.cli import main

from .translate import translate


# command group for all doe2 extension commands.
@click.group(help='dragonfly doe2 commands.')
@click.version_option()
def doe2():
    pass


doe2.add_command(translate)

# add doe2 sub-commands to df CLI
main.add_command(doe2)
