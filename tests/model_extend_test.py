# coding=utf-8
from dragonfly_doe2.properties.model import ModelDOE2Properties

from dragonfly.model import Model

from tests.fixtures.model import two_buildings


def test_doe2_properties():
    """Test the existence of the Model DOE2 properties."""
    model = two_buildings()

    assert hasattr(model.properties, 'doe2')
    assert isinstance(model.properties.doe2, ModelDOE2Properties)
    str(model.properties.doe2)  # test the string representation
    assert isinstance(model.properties.host, Model)


def test_duplicate():
    """Test the duplicate method."""
    model = two_buildings()
    new_model = model.duplicate()
    assert new_model is not model


def test_to_from_dict():
    """Test the Model to_dict and from_dict methods."""
    model = two_buildings()

    model_dict = model.to_dict()

    assert 'doe2' in model_dict['properties']

    new_model = Model.from_dict(model_dict)
    assert isinstance(new_model, Model)
