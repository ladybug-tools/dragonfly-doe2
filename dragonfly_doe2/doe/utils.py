import re


def short_name(name, max_length):
    if len(name) <= max_length:
        return name

    shortened_name = ''.join(re.split('[aeiouy\-\_]', name))

    if len(shortened_name) <= max_length:
        return shortened_name

    shortened_name = ''.join(shortened_name.split())
    if len(shortened_name) > max_length:
        raise ValueError(
            f'{name} cannot be shorten to fit the eQuest limitation of 32 characters. '
            'You need to change the name manually to be shorter than 32 characters.'
        )
    return shortened_name


def lower_left_properties(room_2d):
    """Get the vertices, boundary conditions and windows starting from lower left."""
    floor_geo = room_2d.floor_geometry
    start_pt = floor_geo.vertices[0]
    min_y, min_x, pt_i = start_pt.y, start_pt.x, 0
    for i, pt in enumerate(floor_geo.vertices):
        if pt.y < min_y:
            min_y, min_x = pt.y, pt.x
            pt_i = i
        elif pt.y == min_y:
            if pt.x < min_x:
                min_y, min_x = pt.y, pt.x
                pt_i = i
    verts = floor_geo.vertices[pt_i:] + floor_geo.vertices[:pt_i]
    bcs = room_2d.boundary_conditions[pt_i:] + room_2d.boundary_conditions[:pt_i]
    w_par = room_2d.window_parameters[pt_i:] + room_2d.window_parameters[:pt_i]
    return (verts, bcs, w_par)

#doe2_verts, doe2_bcs, doe2_windows = lower_left_properties(room_2d)
