"""Test the CLI commands"""
import os
from click.testing import CliRunner

from dragonfly_doe2.cli.translate import model_to_inp_cli


def test_model_to_folder():
    runner = CliRunner()
    input_df_model = './tests/assets/model_complete_simple.dfjson'
    out_file = './tests/assets/model_complete_simple.inp'
    hvac_mapping = 'Story'

    in_args = [
        input_df_model, '--hvac-mapping', hvac_mapping,
        '--exclude-interior-walls',  '--exclude-interior-ceilings',
        '--output-file', out_file]
    result = runner.invoke(model_to_inp_cli, in_args)

    assert result.exit_code == 0
    assert os.path.isfile(out_file)
    os.remove(out_file)
