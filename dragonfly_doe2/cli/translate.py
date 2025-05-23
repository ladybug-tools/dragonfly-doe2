"""dragonfly doe2 translation commands."""
import click
import sys
import logging
import json

from ladybug.commandutil import process_content_to_output
from dragonfly.model import Model
from honeybee_doe2.simulation import SimulationPar

from dragonfly_doe2.writer import model_to_inp as writer_model_to_inp

_logger = logging.getLogger(__name__)


@click.group(help='Commands for translating Dragonfly files to DOE-2.')
def translate():
    pass


@translate.command('model-to-inp')
@click.argument('model-file', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--multiplier/--full-geometry', ' /-fg', help='Flag to note if the '
    'multipliers on each Building story will be passed along to the '
    'generated Honeybee Room objects or if full geometry objects should be '
    'written for each story in the building.', default=True, show_default=True)
@click.option(
    '--plenum/--no-plenum', '-p/-np', help='Flag to indicate whether '
    'ceiling/floor plenum depths assigned to Room2Ds should generate '
    'distinct 3D Rooms in the translation.', default=True, show_default=True)
@click.option(
    '--ceil-adjacency/--no-ceil-adjacency', '-a/-na', help='Flag to indicate '
    'whether adjacencies should be solved between interior stories when '
    'Room2Ds perfectly match one another in their floor plate. This ensures '
    'that Surface boundary conditions are used instead of Adiabatic ones. '
    'Note that this input has no effect when the object-per-model is Story.',
    default=True, show_default=True)
@click.option(
    '--sim-par-json', '-sp', help='Full path to a honeybee-doe2 SimulationPar '
    'JSON that describes all of the settings for the simulation. If unspecified, '
    'default parameters will be generated.', default=None, show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--hvac-mapping', '-hm', help='Text to indicate how HVAC systems should be '
    'assigned to the exported model. Story will assign one HVAC system for each '
    'distinct level polygon, Model will use only one HVAC system for the whole model '
    'and AssignedHVAC will follow how the HVAC systems have been assigned to the'
    'Rooms.properties.energy.hvac. Choose from: Room, Story, Model, AssignedHVAC',
    default='Story', show_default=True, type=str)
@click.option(
    '--include-interior-walls/--exclude-interior-walls', ' /-xw', help='Flag to note '
    'whether interior walls should be excluded from the export.',
    default=True, show_default=True)
@click.option(
    '--include-interior-ceilings/--exclude-interior-ceilings', ' /-xc', help='Flag to '
    'note whether interior ceilings should be excluded from the export.',
    default=True, show_default=True)
@click.option(
    '--equest-version', '-eq', help='Optional text string to denote the version '
    'of eQuest for which the INP definition will be generated. If unspecified '
    'or unrecognized, the latest version of eQuest will be used.',
    default='3.65', show_default=True, type=str)
@click.option(
    '--output-file', '-o', help='Optional INP file path to output the INP string '
    'of the translation. By default this will be printed out to stdout.',
    type=click.File('w'), default='-', show_default=True)
def model_to_inp_cli(
    model_file, multiplier, plenum, ceil_adjacency, sim_par_json, hvac_mapping,
    include_interior_walls, include_interior_ceilings, equest_version, output_file
):
    """Translate a Dragonfly Model file to a Radiance string.

    The resulting string will include all geometry and all modifiers.

    \b
    Args:
        model_file: Full path to a Dragonfly Model JSON or Pkl file.
    """
    try:
        full_geometry = not multiplier
        no_plenum = not plenum
        no_ceil_adjacency = not ceil_adjacency
        exclude_interior_walls = not include_interior_walls
        exclude_interior_ceilings = not include_interior_ceilings
        model_to_inp(
            model_file, full_geometry, no_plenum, no_ceil_adjacency,
            sim_par_json, hvac_mapping,
            exclude_interior_walls, exclude_interior_ceilings,
            equest_version, output_file)
    except Exception as e:
        _logger.exception('Model translation failed.\n{}\n'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


def model_to_inp(
    model_file, full_geometry=False, no_plenum=False, no_ceil_adjacency=False,
    sim_par_json=None, hvac_mapping='Story', exclude_interior_walls=False,
    exclude_interior_ceilings=False, equest_version=None, output_file=None,
    multiplier=True, plenum=True, ceil_adjacency=True,
    include_interior_walls=True, include_interior_ceilings=True
):
    """Translate a Model file to an INP string.

    Args:
        model_file: Full path to a Model JSON file (DFJSON) or a Model pkl (DFpkl) file.
        full_geometry: Boolean to note if the multipliers on each Building story
            will be passed along to the generated Honeybee Room objects or if
            full geometry objects should be written for each story in the
            building. (Default: False).
        no_plenum: Boolean to indicate whether ceiling/floor plenum depths
            assigned to Room2Ds should generate distinct 3D Rooms in the
            translation. (Default: False).
        ceil_adjacency: Boolean to indicate whether adjacencies should be solved
            between interior stories when Room2Ds perfectly match one another
            in their floor plate. This ensures that Surface boundary conditions
            are used instead of Adiabatic ones. Note that this input has no
            effect when the object-per-model is Story. (Default: False).
        simulation_par: A honeybee-doe2 SimulationPar object to specify how the
            DOE-2 simulation should be run. If None, default simulation
            parameters will be generated, which will run the simulation for the
            full year. (Default: None).
        hvac_mapping: Text to indicate how HVAC systems should be assigned to the
            exported model. Story will assign one HVAC system for each distinct
            level polygon, Model will use only one HVAC system for the whole model
            and AssignedHVAC will follow how the HVAC systems have been assigned
            to the Rooms.properties.energy.hvac. Choose from the options
            below. (Default: Story).

            * Room
            * Story
            * Model
            * AssignedHVAC

        exclude_interior_walls: Boolean to note whether interior wall Faces
            should be excluded from the resulting string. (Default: False).
        exclude_interior_ceilings: Boolean to note whether interior ceiling
            Faces should be excluded from the resulting string. (Default: False).
        equest_version: An optional text string to denote the version of eQuest
            for which the INP definition will be generated. If unspecified
            or unrecognized, the latest version of eQuest will be used.
        output_file: Optional INP file to output the INP string of the translation.
            If None, the string will be returned from this method. (Default: None).
    """
    # re-serialize the Dragonfly Model
    model = Model.from_file(model_file)

    # load simulation parameters if specified
    sim_par = None
    if sim_par_json is not None:
        with open(sim_par_json) as json_file:
            data = json.load(json_file)
        sim_par = SimulationPar.from_dict(data)

    # create the strings for the model
    multiplier = not full_geometry
    ceil_adjacency = not no_ceil_adjacency
    inp_str = writer_model_to_inp(
        model, multiplier, no_plenum, ceil_adjacency, sim_par, hvac_mapping,
        exclude_interior_walls, exclude_interior_ceilings, equest_version)

    # write out the INP file
    return process_content_to_output(inp_str, output_file)
