"""Dragonfly DOE2 Translation Commands"""
import click
import sys
import pathlib
import logging

from ..writer import model_to_inp
from dragonfly.model import Model
from honeybee.model import Model as HBModel


_logger = logging.getLogger(__name__)


@click.group(help='Commands for translating Dragonfly JSON files to *.inp files.')
def translate():
    pass


@translate.command('dfjson-to-inp')
@click.argument('df-json', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True)
)
@click.option('--name', '-n', help='Name of the output file.', default="model",
              show_default=True
              )
@click.option('--folder', '-f', help='Path to target folder.', type=click.Path(
    exists=False, file_okay=False, resolve_path=True, dir_okay=True),
    default='.', show_default=True
)
def df_model_to_inp_file(df_json, name, folder):
    """Translate a DFJSON into a doe2 *.inp file."""
    try:
        model = Model.from_dfjson(dfjson_file=df_json)
        folder = pathlib.Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        model_to_inp(model, folder=folder, name=name)
    except Exception as e:
        _logger.exception(f'Model translation failed.\n{e}')
        sys.exit(1)
    else:
        sys.exit(0)


@translate.command('hbjson-to-inp')
@click.argument('hb-json', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True)
)
@click.option('--name', '-n', help='Name of the output file.', default="model",
              show_default=True
              )
@click.option('--folder', '-f', help='Path to target folder.', type=click.Path(
    exists=False, file_okay=False, resolve_path=True, dir_okay=True),
    default='.', show_default=True
)
def hb_model_to_inp_file(hb_json, name, folder):
    """Translate a HBJSON into a doe2 *.inp file."""
    try:
        hb_model = HBModel.from_file(hb_json)
        model = Model.from_honeybee(hb_model)
        folder = pathlib.Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        model_to_inp(model, folder=folder, name=name)
    except Exception as e:
        _logger.exception(f'Model translation failed.\n{e}')
        sys.exit(1)
    else:
        sys.exit(0)
