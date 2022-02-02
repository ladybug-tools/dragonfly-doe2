import os

from click.testing import CliRunner
from ladybug.futil import nukedir

from dragonfly_doe2.cli.translate import df_model_to_inp_file


def test_model_to_folder():
    runner = CliRunner()
    input_df_model = './assets/reference_dfm/complex_model_with_bcs.dfjson'
    folder = '.assets/sample_out'
    name = 'cli_test'

    result = runner.invoke(
        df_model_to_inp_file, [input_df_model, '--folder', folder, '--name', name]
    )
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(folder, f'{name}.inp'))
    nukedir(folder, True)
