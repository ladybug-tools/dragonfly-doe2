"""dragonfly-doe2 commands which will be added to the dragonfly CLI."""
import click

from dragonfly.cli import main
from .translate import translate


# command group for all doe2 extension commands.
@click.group(help='dragonfly doe2 commands.')
def doe2():
    pass


# add sub-commands for doe2
doe2.add_command(translate)

# add doe2 sub-commands to dragonfly CLI
main.add_command(doe2)
