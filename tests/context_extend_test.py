from dragonfly_doe2.properties.context import ContextShadeDOE2Properties

from dragonfly.context import ContextShade

from tests.fixtures.context import default_context, custom_context


def test_doe2_properties():
    """Test the existence of the ContextShade DOE2 properties."""
    context = default_context()

    assert hasattr(context.properties, 'doe2')
    assert isinstance(context.properties.doe2, ContextShadeDOE2Properties)
    str(context.properties.doe2)  # test the string representation
    assert isinstance(context.properties.host, ContextShade)


def test_duplicate():
    """Test the duplicate method."""
    context = custom_context()
    new_context = context.duplicate()
    assert new_context is not context


def test_to_from_dict():
    """Test the Building to_dict and from_dict methods."""
    context = custom_context()

    context_dict = context.to_dict()

    assert 'doe2' in context_dict['properties']

    new_context = ContextShade.from_dict(context_dict)
    assert isinstance(new_context, ContextShade)
