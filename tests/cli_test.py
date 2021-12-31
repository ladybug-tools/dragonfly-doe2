import os

from click.testing import CliRunner
from ladybug.futil import nukedir

from dragonfly_doe2.cli.translate import model_to_inp


def test_model_to_folder():
    runner = CliRunner()
    input_df_model = './assets/test_output_inps/test-model2.inp'
    folder = '.assets/temp'
    name = 'cli_test_45'  # dunno what the n45 is; just copying..

    result = runner.invoke(
        model_to_inp, [input_df_model, '--folder', folder, '--name', name]
    )
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(folder, f'{name}.inp'))
    nukedir(folder, True)
