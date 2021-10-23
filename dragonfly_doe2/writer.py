"""Methods to write files for DOE-2 simulation."""

# TODO:   Make a 'main file def' to pass as an arg\
# TODO: into the objs to then add in correct loc blocks
from dragonfly import room2d, story


def room2d_to_doe2(room2d):
    """Generate a DOE-2 INP string for a Room2D.

    Args:
        room2d: A dragonfly Room2D for which an INP file string will be returned.

    Returns:
        A INP text string which can be written into an .inp file.


        May move away from this due to doe2 file 'block' obj organization
    """
    # TODO: Add some more code here to generate the .inp file string
    # Prolly use more touples tbh for each room tbh and in the building to doe2:
    # Sort by story for each *.inp block obj and not have to do oopyness

    # so this would return  a touple for each room based *.inp block in a list
    pass


def story_to_doe2(story):
    """Generate a DOE-2 INP string for a Story.

    Args:
        story: A dragonfly Story for which an INP file string will be returned.

    Returns:
        A INP text string which can be written into an .inp file.
    """
    # TODO: Add some more code here to generate the .inp file string
    return ''


def building_to_doe2(building):
    """Generate a DOE-2 INP string for a Building.

    The resulting string will include all geometry (Room2Ds and Stories) and can
    be written to an INP file.

    Args:
        building: A dragonfly Building for which an INP file string will be returned.

    Returns:
        A INP text string which can be written into an .inp file.
    """
    # TODO: Add some more code here to generate the .inp file string

    # write all of the geometry
    bldg_str = ['!-   ============ BUILDING GEOMETRY ============\n']
    for story in building.all_stories():
        bldg_str.append(story.to.doe2(story))
        for room in story.room_2ds:
            bldg_str.append(room.to.doe2(room))

    return '\n\n'.join(bldg_str)


def model_to_doe2(model):
    """Generate a list of DOE-2 INP strings from a Model.

    There will be one string per Building and each can be written to an INP file.

    Args:
        model: A dragonfly Model for which INP file string will be returned.

    Returns:
        A list of INP text strings which can each be written into an .inp file.
    """
    # convert the Model to Feet because DOE-2 is ancient and uses IP
    if model.units != 'Feet':
        model = model.duplicate()  # duplicate the model to avoid mutating the input
        model.convert_to_units('Feet')

    # TODO: Add some code here to generate the .inp file string

    # write all of the buildings
    building_strs = []
    for bldg in model.buildings:
        building_strs.append(bldg.to.doe2(bldg))

    # write all context shade geometry
    shd_str = ['!-   ========== CONTEXT GEOMETRY ==========\n']
    for shade in model.context_shades:
        shd_str.append(shade.to.doe2(shade))
    shd_str = '\n\n'.join(shd_str)

    # join the building and shade strings
    inp_strs = []
    for bldg_str in building_strs:
        inp_strs.append('\n\n'.join((bldg_str, shd_str)))
    return inp_strs


def poly_str(_df_obj):
    if isinstance(_df_obj, room2D):
        header = '"{} Plg" = POLYGON\n   '.format(_hst.display_name)
        vert_strs = []
        for obj in _obj:
            vstr = 'V{}'.format(obj[0])+(' '*15) + \
                '= ( {} , {} )\n   '.format(obj[1], obj[2])
            vert_strs.append(vstr)

        for obj in vert_strs:
            header = header + obj
    elif isinstance(_df_obj, story):
        header = '"{} Plg" = POLYGON\n   '.format(_hst.display_name)
        vert_strs = []
        for obj in _obj:
            vstr = 'V{}'.format(obj[0])+(' '*15) + \
                '= ( {} , {} )\n   '.format(obj[1], obj[2])
            vert_strs.append(vstr)

        for obj in vert_strs:
            header = header + obj
    return(header)
