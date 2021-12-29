import pathlib
import sys
import os

from dragonfly_doe2.writer import model_to_inp
from dragonfly.model import Model


def main():
    df_json = 'assets/reference_dfm/complex_model.dfjson'
    out_inp = 'assets/test_output_inps'
    out_file = pathlib.Path(out_inp, 'test-model.inp')
    df_model = Model.from_dfjson(dfjson_file=df_json)
    a = model_to_inp(df_model, folder=out_inp, name='test-model.inp')
    a


if __name__ == '__main__':
    main()
