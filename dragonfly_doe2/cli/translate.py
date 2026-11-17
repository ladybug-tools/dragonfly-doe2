"""dragonfly doe2 translation commands."""
import click
import sys
import logging
import json

from ladybug.commandutil import process_content_to_output
from ladybug.projectinfo import ProjectInfo
from dragonfly.model import Model
from honeybee_doe2.simulation import SimulationPar
from honeybee_doe2.reader import model_from_inp_file

from dragonfly_doe2.writer import model_to_inp as writer_model_to_inp

_logger = logging.getLogger(__name__)


@click.group(help='Commands for translating Dragonfly files to DOE-2.')
def translate():
    pass


@translate.command('model-to-inp')
@click.argument('model-file', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--sim-par-json', '-sp', help='Full path to a honeybee-doe2 SimulationPar '
    'JSON that describes all of the settings for the simulation. If unspecified, '
    'default parameters will be generated.', default=None, show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--project-info', '-pi', help='Full path to a ladybug ProjectInfo JSON that '
    'describes criteria about the project site. This will be used to fill in any '
    'information that is not described in the --sim-par-json. Otherwise, '
    '--sim-par-json overrides whatever is specified within the --project-info.',
    default=None, show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
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
    '--merge-method', '-m', help='Text to describe how the Room2Ds should '
    'be merged into individual Rooms during the translation. Specifying a '
    'value here can be an effective way to reduce the number of Room '
    'volumes in the resulting Model and, ultimately, yield a faster simulation '
    'time with less results to manage. Choose from: None, Zones, PlenumZones, '
    'Stories, PlenumStories.', type=str, default='None', show_default=True)
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
    '--face-rename-format', '-fn', help='Optional text for the pattern '
    'with which faces will be renamed. Any property on the honeybee Face class '
    'may be used (eg. gbxml_str) and each property should be put in curly '
    'brackets. Nested properties can be specified by using "." to denote '
    'nesting levels (eg. properties.energy.construction.display_name). '
    'Functions that return string outputs can also be passed here as long '
    'as these functions defaults specified for all arguments.',
    type=str, show_default=True,
    default="{parent.display_name} - {gbxml_type} - {cardinal_direction}")
@click.option(
    '--subface-rename-format', '-sfn', help='Optional text for the pattern '
    'with which apertures and doors will be renamed. Any property that exists '
    'on both the honeybee Aperture and honeybee Door class may be used '
    '(eg. type) and each property should be put in curly brackets. Nested '
    'properties can be specified by using "." to denote nesting levels '
    '(eg. properties.energy.construction.display_name). Functions that '
    'return string outputs can also be passed here as long as these '
    'functions defaults specified for all arguments.',
    type=str, show_default=True,
    default="{parent.parent.display_name} - {type} - {cardinal_direction}")
@click.option(
    '--name-decimal-count', '-dc', help='An integer to set the number of '
    'decimal places that appear in face and sub-face names for all numerical '
    'properties. If None, the number of decimal places are determined by the '
    'model tolerance.', type=int, default=None, show_default=True)
@click.option(
    '--include-units-in-name/--exclude-units-in-name', ' /-xu', help='Flag '
    'to note whether the units should be excluded from all length, area '
    'and volume attributes.', default=True, show_default=True)
@click.option(
    '--output-file', '-o', help='Optional INP file path to output the INP string '
    'of the translation. By default this will be printed out to stdout.',
    type=click.File('w'), default='-', show_default=True)
def model_to_inp_cli(
    model_file, sim_par_json, project_info,
    multiplier, plenum, ceil_adjacency, merge_method,
    hvac_mapping, include_interior_walls, include_interior_ceilings,
    equest_version, face_rename_format, subface_rename_format,
    name_decimal_count, include_units_in_name, output_file
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
        exclude_units_in_name = not include_units_in_name
        model_to_inp(
            model_file, sim_par_json, project_info,
            full_geometry, no_plenum, no_ceil_adjacency, merge_method,
            hvac_mapping, exclude_interior_walls, exclude_interior_ceilings,
            equest_version, face_rename_format, subface_rename_format,
            name_decimal_count, exclude_units_in_name, output_file
        )
    except Exception as e:
        _logger.exception('Model translation failed.\n{}\n'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


def model_to_inp(
    model_file, sim_par_json=None, project_info=None,
    full_geometry=False, no_plenum=False, no_ceil_adjacency=False,
    merge_method='None', hvac_mapping='Story',
    exclude_interior_walls=False, exclude_interior_ceilings=False,
    equest_version=None,
    face_rename_format='{parent.display_name} - {gbxml_type} - {cardinal_direction}',
    subface_rename_format='{parent.parent.display_name} - {type} - {cardinal_direction}',
    name_decimal_count=None, exclude_units_in_name=False,
    output_file=None,
    multiplier=True, plenum=True, ceil_adjacency=True,
    include_interior_walls=True, include_interior_ceilings=True
):
    """Translate a Model file to an INP string.

    Args:
        model_file: Full path to a Model JSON file (DFJSON) or a Model pkl (DFpkl) file.
        sim_par_json: A honeybee-doe2 SimulationPar object to specify how the
            DOE-2 simulation should be run. If None, default simulation
            parameters will be generated, which will run the simulation for the
            full year. (Default: None).
        project_info: Full path to a ladybug ProjectInfo JSON that describes criteria
            about the project site. This will be used to fill in any information that
            is not described in the sim_par_json. Otherwise, the sim_par_json overrides
            whatever is specified within the project_info. (Default: None).
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
        merge_method: An optional text string to describe how the Room2Ds should
            be merged into individual Rooms during the translation. Specifying a
            value here can be an effective way to reduce the number of Room
            volumes in the resulting Model and, ultimately, yield a faster simulation
            time with less results to manage. Note that Room2Ds will only be merged if
            they form a contiguous volume. Otherwise, there will be multiple Rooms per
            zone or story, each with an integer added at the end of their
            identifiers. Choose from the following options:

            * None - No merging will occur
            * Zones - Room2Ds in the same zone will be merged
            * PlenumZones - Only plenums in the same zone will be merged
            * Stories - Rooms in the same story will be merged
            * PlenumStories - Only plenums in the same story will be merged
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
        face_rename_format: An optional text string for the pattern with which
            faces will be renamed. Any property on the honeybee Face class may be
            used (eg. gbxml_str) and each property should be put in curly brackets.
            Nested properties can be specified by using "." to denote nesting levels
            (eg. properties.energy.construction.display_name). Functions that
            return string outputs can also be passed here as long as these
            functions defaults specified for all arguments. If None, the names
            will match the identifiers.
        subface_rename_format: An optional text string for the pattern with which
            apertures and doors will be renamed. Any property that exists on both
            the honeybee Aperture and honeybee Door class may be used (eg. gbxml_type)
            and each property should be put in curly brackets. Nested
            properties can be specified by using "." to denote nesting levels
            (eg. properties.energy.construction.display_name). Functions that
            return string outputs can also be passed here as long as these
            functions defaults specified for all arguments. If None, the names
            will match the identifiers.
        name_decimal_count: An integer to set the number of decimal places that
            appear in face and opening names for all numerical properties.
            If None, the number of decimal places are determined by the
            model tolerance. (Default: None).
        exclude_units_in_name: Boolean for wether the units should be
            excluded from all length, area and volume attributes. (Default: False).
        output_file: Optional INP file to output the INP string of the translation.
            If None, the string will be returned from this method. (Default: None).
    """
    # re-serialize the input files
    if project_info is not None:
        project_info = ProjectInfo.from_json(project_info)
    sim_par = None
    if sim_par_json is not None:
        with open(sim_par_json) as json_file:
            data = json.load(json_file)
        sim_par = SimulationPar.from_dict(data)
    model = Model.from_file(model_file)

    # create the strings for the model
    multiplier = not full_geometry
    ceil_adjacency = not no_ceil_adjacency
    inp_str = writer_model_to_inp(
        model, sim_par, project_info,
        multiplier, no_plenum, ceil_adjacency, merge_method,
        hvac_mapping, exclude_interior_walls, exclude_interior_ceilings,
        equest_version, face_rename_format, subface_rename_format,
        name_decimal_count, exclude_units_in_name
    )

    # write out the INP file
    return process_content_to_output(inp_str, output_file)


@translate.command('model-from-inp')
@click.argument('inp-file', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--conversion-method', '-c', help='Text to indicate how to convert '
    'the 3D Rooms to Dragonfly Room2D. Choose from: AllRoom2D, ExtrudedOnly, AllRoom3D.',
    type=str, default="ExtrudedOnly", show_default=True)
@click.option(
    '--output-file', '-o', help='Optional DFJSON file path to output the file string '
    'of the translation. By default this will be printed out to stdout.',
    type=click.File('w'), default='-', show_default=True)
def model_from_inp_cli(inp_file, conversion_method, output_file):
    """Translate an INP file to a Dragonfly Model as a DFJSON.

    \b
    Args:
        inp_file: Full path to an INP file.
    """
    try:
        model_from_inp(inp_file, conversion_method, output_file)
    except Exception as e:
        _logger.exception(f'Model translation failed:\n{e}')
        sys.exit(1)
    else:
        sys.exit(0)


def model_from_inp(inp_file, conversion_method='ExtrudedOnly', output_file=None):
    """Translate an INP file to a Dragonfly Model as a DFJSON.

    Args:
        inp_file: Full path to an INP file.
        conversion_method: Text to indicate how to convert the 3D Rooms to
            Dragonfly Room2D. Choose from: AllRoom2D, ExtrudedOnly, AllRoom3D.
        output_file: Optional DFJSON file path to output the string of the
            translation. If None, the string will be returned from this function.
    """
    hb_model = model_from_inp_file(inp_file)
    df_model = Model.from_honeybee(hb_model, conversion_method)
    content_str = json.dumps(df_model.to_dict())
    return process_content_to_output(content_str, output_file)
