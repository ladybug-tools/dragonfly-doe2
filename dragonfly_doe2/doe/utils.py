import re
import ladybug_geometry.geometry2d as lbtg2
import ladybug_geometry.geometry3d as lbtg3
from ladybug_geometry.geometry2d.pointvector import Point2D, Vector2D
from ladybug_geometry.geometry2d.polygon import Polygon2D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.plane import Plane


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


def bottom_left_counter_clockwise_vertices(geom):
    """Get this face's vertices starting from the bottom left and moving counterclockwise.
    This is useful for getting the vertices of several faces aligned with the
    same global geometry rules for export to engines like EnergyPlus.
    """
    if geom._plane.n.z == 1 or geom._plane.n.z == -1:  # no vertex is above another
        return geom.vertices if not geom.is_clockwise \
            else tuple(reversed(geom.vertices))
    # get a 2d polygon in the face plane that has a positive Y axis.
    proj_y = Vector3D(0, 0, 1).project(geom._plane.n)
    proj_x = proj_y.rotate(geom._plane.n, math.pi / -2)
    ref_plane = Plane(geom._plane.n, geom._plane.o, proj_x)
    polygon = Polygon2D(tuple(ref_plane.xyz_to_xy(v) for v in geom._vertices))
    # get counterclockwise vertices
    if geom.is_clockwise:
        verts3d = tuple(reversed(geom.vertices))
        verts2d = tuple(reversed(polygon.vertices))
    else:
        verts3d = geom.vertices
        verts2d = polygon.vertices
    # sort points so that they start with the upper left point
    corner_pt = Point2D(polygon.min.x, polygon.min.y)
    return geom._corner_pt_verts(corner_pt, verts3d, verts2d)
