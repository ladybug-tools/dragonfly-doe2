"""Write an inp file from a Dragonfly model."""
import pathlib
from dragonfly.model import Model as DFModel
from .doe.model import Model


def model_to_inp(
        model: DFModel, folder: str = '.', name: str = None) -> pathlib.Path:
    """Export a dragonfly model to a Doe2 INP file.

    Args:
        model: A Dragonfly model.
        folder: Path to target folder to export the file. Default is current folder.
        name: An optional name for exported file. By default the name of the model will
            be used.

    Returns:
        Path to exported inp file.
    """

    # TODO: add all the other arguments that one might to pass to the model
    inp_model = Model.from_df_model(model)

    # write to inp
    name = name or model.display_name
    if not name.lower().endswith('.inp'):
        name = f'{name}.inp'
    out_folder = pathlib.Path(folder)
    out_folder.mkdir(parents=True, exist_ok=True)
    out_file = out_folder.joinpath(name)
    out_file.write_text(inp_model.to_inp())
    return out_file
