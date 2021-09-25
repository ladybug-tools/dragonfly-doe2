from dragonfly.room2d import Room2D
from dragonfly.windowparameter import SimpleWindowRatio
from dragonfly.shadingparameter import Overhang
from honeybee.boundarycondition import boundary_conditions as bcs
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D

from dragonfly_doe2.properties.room2d import Room2DDOE2Properties


def test_doe2_properties():
    """Test the existence of the Building DOE2 properties."""
    pts = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    ashrae_base = SimpleWindowRatio(0.4)
    overhang = Overhang(1)
    boundarycs = (bcs.outdoors, bcs.ground, bcs.outdoors, bcs.ground)
    window = (ashrae_base, None, ashrae_base, None)
    shading = (overhang, None, None, None)
    room = Room2D('SquareShoebox', Face3D(pts), 3, boundarycs, window, shading)

    assert hasattr(room.properties, 'doe2')
    assert isinstance(room.properties.doe2, Room2DDOE2Properties)
