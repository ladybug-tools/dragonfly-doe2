"""Dragonfly DOE2 Translation Commands"""
import click
import sys
import pathlib
import logging

from .writer import model_to_inp
from dragonfly.models import Model

_logger = logging.addLevelName(__name__)


@click.group(help='Commands for translating Dragonfly JSON files to *.inp files.')
def translate():
    pass


@translate.command('model-to-inp')
@click.argument('model-json', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True)
)
@click.option('--name', '-n', help='Name of the output file.', default="model",
              show_default=True
              )
@click.option('--folder', '-f', help='Path to target folder.', type=click.Path(
    exists=False, file_okay=False, resolve_path=True, dir_okay=True),
    default='.', show_default=True
)
def model_to_inp(df_json, name, folder):
    """Translate a df_model.dfjson into a doe2 *.inp file."""
    try:
        model = Model.from_dfjson(dfjson_file=df_json)
        folder = pathlib.Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        made_model = model_to_inp(model, folder=folder, name=name)
    except Exception as e:
        _logger.exception(f'Model translation failed.\n{e}')
        sys.exit(1)
    else:
        sys.exit(0)
