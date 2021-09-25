# coding=utf-8
"""Model DOE2 Properties."""

from dragonfly.extensionutil import model_extension_dicts


class ModelDOE2Properties(object):
    """DOE2 Properties for Dragonfly Model.

    Args:
        host: A dragonfly_core Model object that hosts these properties.

    Properties:
        * host
    """

    __slots__ = ('_host',)

    def __init__(self, host):
        """Initialize Model DOE2 properties."""
        self._host = host

    @property
    def host(self):
        """Get the Model object hosting these properties."""
        return self._host

    def apply_properties_from_dict(self, data):
        """Apply the DOE2 properties of a dictionary to the host Model of this object.

        Args:
            data: A dictionary representation of an entire dragonfly-core Model.
                Note that this dictionary must have ModelDOE2Properties in order
                for this method to successfully apply the DOE2 properties.
        """
        # check that DOE2 properties exist and apply the global ones to this object
        assert 'doe2' in data['properties'], \
            'Dictionary possesses no ModelDOE2Properties.'

        # collect lists of doe2 property dictionaries
        building_d_dicts, story_d_dicts, room2d_d_dicts, context_d_dicts = \
            model_extension_dicts(data, 'doe2', [], [], [], [])

        # apply doe2 properties to objects using the doe2 property dictionaries
        for bldg, b_dict in zip(self.host.buildings, building_d_dicts):
            if b_dict is not None:
                bldg.properties.doe2.apply_properties_from_dict(b_dict)
        for story, s_dict in zip(self.host.stories, story_d_dicts):
            if s_dict is not None:
                story.properties.doe2.apply_properties_from_dict(s_dict)
        for room, r_dict in zip(self.host.room_2ds, room2d_d_dicts):
            if r_dict is not None:
                room.properties.doe2.apply_properties_from_dict(r_dict)
        for shade, s_dict in zip(self.host.context_shades, context_d_dicts):
            if s_dict is not None:
                shade.properties.doe2.apply_properties_from_dict(s_dict)

    def to_dict(self):
        """Return Model DOE2 properties as a dictionary."""
        base = {'doe2': {'type': 'ModelDOE2Properties'}}
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this Model.

        Args:
            new_host: A new Model object that hosts these properties.
                If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        new_obj = ModelDOE2Properties(_host)
        return new_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Model DOE2 Properties: {}'.format(self.host.identifier)
