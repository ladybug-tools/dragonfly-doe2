"""Methods to write files for DOE-2 simulation."""


def room2d_to_doe2(room2d):
    """Generate a DOE-2 INP string for a Room2D.

    Args:
        room2d: A dragonfly Room2D for which an INP file string will be returned.

    Returns:
        A INP text string which can be written into an .inp file.
    """
    # TODO: Add some more code here to generate the .inp file string
    return ''


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
