"""Tests the features that dragonfly_doe2 adds to dragonfly_core Room2D."""
from ladybug_geometry.geometry3d import Point3D, Face3D
from dragonfly.model import Model
from dragonfly.building import Building
from dragonfly.story import Story
from dragonfly.room2d import Room2D
from dragonfly.roof import RoofSpecification
from dragonfly.windowparameter import SimpleWindowRatio


def test_model_properties_to_honeybee():
    """Test translation of DOE-2 properties to Honeybee."""
    # Crate an input Model
    pts1 = (Point3D(0, 0, 0), Point3D(10, 0, 0),
            Point3D(10, 10, 0), Point3D(0, 10, 0))
    pts2 = (Point3D(10, 0, 0), Point3D(20, 0, 0),
            Point3D(20, 10, 0), Point3D(10, 10, 0))
    pts3 = (Point3D(0, 0, 3.25), Point3D(20, 0, 3.25),
            Point3D(20, 5, 5), Point3D(0, 5, 5))
    pts4 = (Point3D(0, 5, 5), Point3D(20, 5, 5),
            Point3D(20, 10, 3.25), Point3D(0, 10, 3.25))
    room2d_full = Room2D(
        'R1-full', floor_geometry=Face3D(pts1), floor_to_ceiling_height=4,
        is_ground_contact=True, is_top_exposed=True)
    room2d_plenum = Room2D(
        'R2-plenum', floor_geometry=Face3D(pts2), floor_to_ceiling_height=4,
        is_ground_contact=True, is_top_exposed=True)
    room2d_plenum.ceiling_plenum_depth = 1.0
    roof = RoofSpecification([Face3D(pts3), Face3D(pts4)])
    story = Story('S1', [room2d_full, room2d_plenum])
    story.roof = roof
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(SimpleWindowRatio(0.4))
    building = Building('Office_Building_1234', [story])
    model = Model('NewDevelopment1', [building])

    room2d_full.properties.doe2.assigned_flow = 100
    room2d_full.properties.doe2.flow_per_area = 1
    room2d_full.properties.doe2.min_flow_ratio = 0.3
    room2d_full.properties.doe2.min_flow_per_area = 0.35
    room2d_full.properties.doe2.hmax_flow_ratio = 0.5

    hb_model = model.to_honeybee('District', None, False, tolerance=0.01)[0]
    room_full = hb_model.rooms[0]

    assert room_full.properties.doe2.assigned_flow == 100
    assert room_full.properties.doe2.flow_per_area == 1
    assert room_full.properties.doe2.min_flow_ratio == 0.3
    assert room_full.properties.doe2.min_flow_per_area == 0.35
    assert room_full.properties.doe2.hmax_flow_ratio == 0.5


def test_model_room_validation():
    """Test the validation of a model with invalid rooms"""
    model_json = './tests/assets/model_with_invalid_rooms.dfjson'
    model = Model.from_dfjson(model_json)

    report = model.properties.doe2.check_for_extension(False, True)
    assert len(report) == 3
    assert report[0]['error_type'] == 'Room Exceeds Maximum Vertex Count'
    assert report[1]['error_type'] == 'Room Exceeds Maximum Vertex Count'
    assert report[2]['error_type'] == 'Room Contains Holes'
