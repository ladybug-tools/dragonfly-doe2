import re
from ladybug.datatype import UNITS as lbt_units, TYPESDICT as lbt_td


def short_name(name, max_length=32):
    if len(name) <= max_length:
        return name

    shortened_name = ''.join(re.split("[aeiouy\\-\\_/]", name))

    if len(shortened_name) <= max_length:
        return shortened_name

    shortened_name = ''.join(shortened_name.split())
    if len(shortened_name) > max_length:
        shortened_name = ''.join(shortened_name.split())
        if len(shortened_name) > max_length:
            raise ValueError(
                f'{name} cannot be shorten to fit the eQuest limitation of 32 characters. ',
                f'Shortens to {shortened_name}\n '
                'You need to change the name manually to be shorter than 32 characters.')
    return shortened_name


def lower_left_properties(room_2d):
    """Get the vertices, boundary conditions and windows starting from lower left.
    v2 WIP
    """
    room_2d.remove_duplicate_vertices()
    simple_w_con = room_2d.properties.energy.construction_set.aperture_set.window_construction.to_simple_construction()
    w_const_name = short_name(simple_w_con.identifier, 32)
    floor_geo = room_2d.floor_geometry
    start_pt = floor_geo.boundary[0]
    min_y, min_x, pt_i = start_pt.y, start_pt.x, 0
    for i, pt in enumerate(floor_geo.boundary):
        if pt.y < min_y:
            min_y, min_x = pt.y, pt.x
            pt_i = i
        elif pt.y == min_y:
            if pt.x < min_x:
                min_y, min_x = pt.y, pt.x
                pt_i = i
    verts = floor_geo.boundary[pt_i:] + floor_geo.boundary[:pt_i]
    if floor_geo.has_holes:
        bcs = room_2d.boundary_conditions[:len(floor_geo.boundary)]
        w_par = room_2d.window_parameters[:len(floor_geo.boundary)]
    else:
        bcs = room_2d.boundary_conditions
        w_par = room_2d.window_parameters
    bcs = bcs[pt_i:] + bcs[:pt_i]
    w_par = w_par[pt_i:] + w_par[:pt_i]

    return (verts, bcs, w_par, w_const_name)


def unit_convertor(value, to_, from_):
    """Helper function to convert values from one unit to another."""
    for key in lbt_units:
        if from_ in lbt_units[key]:
            base_type = lbt_td[key]()
            break
    else:
        raise ValueError(f'Invalid type: {from_}')

    value = base_type.to_unit(value, to_, from_)
    return round(value[0], 3)
