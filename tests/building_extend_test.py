
from dragonfly_doe2.properties.building import BuildingDOE2Properties

from dragonfly.building import Building
from tests.fixtures.building import default_building, custom_building


def test_doe2_properties():
    """Test the existence of the Building DOE2 properties."""
    building = default_building()

    assert hasattr(building.properties, 'doe2')
    assert isinstance(building.properties.doe2, BuildingDOE2Properties)
    str(building.properties.doe2)  # test the string representation
    assert isinstance(building.properties.host, Building)


def test_duplicate():
    """Test the duplicate method."""
    building = custom_building()
    new_building = building.duplicate()
    assert new_building is not building


def test_to_from_dict():
    """Test the Building to_dict and from_dict methods."""
    building = custom_building()

    building_dict = building.to_dict()

    assert 'doe2' in building_dict['properties']
