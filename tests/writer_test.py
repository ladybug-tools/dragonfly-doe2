import pathlib

from dragonfly_doe2.writer import model_to_inp
from dragonfly.model import Model


def test_dfjson_translate():
    """Test translating a DFJSON file to an inp file."""
    df_json = 'assets/reference_dfm/complex_model_with_bcs.dfjson'
    out_inp = 'assets/sample_out'
    out_file = pathlib.Path(out_inp, 'test-model.inp')
    # delete if exist
    if out_file.exists():
        out_file.unlink()
    df_model = Model.from_dfjson(dfjson_file=df_json)
    model_to_inp(df_model, folder=out_inp, name='test-model.inp')

    assert out_file.exists()
    out_file.unlink()
