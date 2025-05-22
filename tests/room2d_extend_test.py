"""Tests the features that dragonfly_doe2 adds to dragonfly_core Room2D."""
from ladybug_geometry.geometry3d import Point3D, Face3D
from honeybee.boundarycondition import boundary_conditions as bcs
from honeybee_energy.lib.programtypes import office_program
from dragonfly.room2d import Room2D
from dragonfly.windowparameter import SimpleWindowRatio
from dragonfly.shadingparameter import Overhang

from dragonfly_doe2.properties.room2d import Room2DDoe2Properties


def test_doe2_properties():
    """Test the existence of the Room2D energy properties."""
    pts = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    ashrae_base = SimpleWindowRatio(0.4)
    overhang = Overhang(1)
    boundarycs = (bcs.outdoors, bcs.ground, bcs.outdoors, bcs.ground)
    window = (ashrae_base, None, ashrae_base, None)
    shading = (overhang, None, None, None)
    room = Room2D('SquareShoebox', Face3D(pts), 3, boundarycs, window, shading)
    room.properties.energy.program_type = office_program
    room.properties.energy.add_default_ideal_air()

    assert hasattr(room.properties, 'doe2')
    assert isinstance(room.properties.doe2, Room2DDoe2Properties)

    assert room.properties.doe2.assigned_flow is None
    room.properties.doe2.assigned_flow = 100
    assert room.properties.doe2.assigned_flow == 100

    assert room.properties.doe2.flow_per_area is None
    room.properties.doe2.flow_per_area = 1
    assert room.properties.doe2.flow_per_area == 1

    assert room.properties.doe2.min_flow_ratio is None
    room.properties.doe2.min_flow_ratio = 0.3
    assert room.properties.doe2.min_flow_ratio == 0.3

    assert room.properties.doe2.min_flow_per_area is None
    room.properties.doe2.min_flow_per_area = 0.35
    assert room.properties.doe2.min_flow_per_area == 0.35

    assert room.properties.doe2.hmax_flow_ratio is None
    room.properties.doe2.hmax_flow_ratio = 0.5
    assert room.properties.doe2.hmax_flow_ratio == 0.5


def test_duplicate():
    """Test what happens to doe2 properties when duplicating a Room2D."""
    pts = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    ashrae_base = SimpleWindowRatio(0.4)
    overhang = Overhang(1)
    boundarycs = (bcs.outdoors, bcs.ground, bcs.outdoors, bcs.ground)
    window = (ashrae_base, None, ashrae_base, None)
    shading = (overhang, None, None, None)
    room_original = Room2D('SquareShoebox', Face3D(pts), 3, boundarycs, window, shading)
    room_original.properties.energy.program_type = office_program
    room_original.properties.energy.add_default_ideal_air()

    room_dup_1 = room_original.duplicate()

    assert room_original.properties.doe2.assigned_flow == \
        room_dup_1.properties.doe2.assigned_flow
    assert room_original.properties.doe2.flow_per_area == \
        room_dup_1.properties.doe2.flow_per_area
    assert room_original.properties.doe2.min_flow_ratio == \
        room_dup_1.properties.doe2.min_flow_ratio
    assert room_original.properties.doe2.min_flow_per_area == \
        room_dup_1.properties.doe2.min_flow_per_area
    assert room_original.properties.doe2.hmax_flow_ratio == \
        room_dup_1.properties.doe2.hmax_flow_ratio

    room_original.properties.doe2.assigned_flow = 100
    room_original.properties.doe2.flow_per_area = 1
    room_original.properties.doe2.min_flow_ratio = 0.3
    room_original.properties.doe2.min_flow_per_area = 0.35
    room_original.properties.doe2.hmax_flow_ratio = 0.5

    assert room_original.properties.doe2.assigned_flow != \
        room_dup_1.properties.doe2.assigned_flow
    assert room_original.properties.doe2.flow_per_area != \
        room_dup_1.properties.doe2.flow_per_area
    assert room_original.properties.doe2.min_flow_ratio != \
        room_dup_1.properties.doe2.min_flow_ratio
    assert room_original.properties.doe2.min_flow_per_area != \
        room_dup_1.properties.doe2.min_flow_per_area
    assert room_original.properties.doe2.hmax_flow_ratio != \
        room_dup_1.properties.doe2.hmax_flow_ratio


def test_to_dict():
    """Test the Room2D to_dict method with doe2 properties."""
    pts = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    ashrae_base = SimpleWindowRatio(0.4)
    overhang = Overhang(1)
    boundarycs = (bcs.outdoors, bcs.ground, bcs.outdoors, bcs.ground)
    window = (ashrae_base, None, ashrae_base, None)
    shading = (overhang, None, None, None)
    room = Room2D('SquareShoebox', Face3D(pts), 3, boundarycs, window, shading)
    room.properties.energy.program_type = office_program
    room.properties.energy.add_default_ideal_air()
    room.properties.doe2.assigned_flow = 100
    room.properties.doe2.flow_per_area = 1
    room.properties.doe2.min_flow_ratio = 0.3
    room.properties.doe2.min_flow_per_area = 0.35
    room.properties.doe2.hmax_flow_ratio = 0.5

    rd = room.to_dict()
    assert 'properties' in rd
    assert rd['properties']['type'] == 'Room2DProperties'
    assert 'doe2' in rd['properties']
    assert rd['properties']['doe2']['type'] == 'Room2DDoe2Properties'
    assert rd['properties']['doe2']['assigned_flow'] == 100
    assert rd['properties']['doe2']['flow_per_area'] == 1
    assert rd['properties']['doe2']['min_flow_ratio'] == 0.3
    assert rd['properties']['doe2']['min_flow_per_area'] == 0.35
    assert rd['properties']['doe2']['hmax_flow_ratio'] == 0.5


def test_from_dict():
    """Test the Room2D from_dict method with doe2 properties."""
    pts = (Point3D(0, 0, 3), Point3D(10, 0, 3), Point3D(10, 10, 3), Point3D(0, 10, 3))
    ashrae_base = SimpleWindowRatio(0.4)
    overhang = Overhang(1)
    boundarycs = (bcs.outdoors, bcs.ground, bcs.outdoors, bcs.ground)
    window = (ashrae_base, None, ashrae_base, None)
    shading = (overhang, None, None, None)
    room = Room2D('SquareShoebox', Face3D(pts), 3, boundarycs, window, shading)
    room.properties.energy.program_type = office_program
    room.properties.energy.add_default_ideal_air()
    room.properties.doe2.assigned_flow = 100
    room.properties.doe2.flow_per_area = 1
    room.properties.doe2.min_flow_ratio = 0.3
    room.properties.doe2.min_flow_per_area = 0.35
    room.properties.doe2.hmax_flow_ratio = 0.5

    rd = room.to_dict()
    new_room = Room2D.from_dict(rd)
    assert new_room.to_dict() == rd
