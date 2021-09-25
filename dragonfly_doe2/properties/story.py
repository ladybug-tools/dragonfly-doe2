# coding=utf-8
"""Story DOE2 Properties."""


class StoryDOE2Properties(object):
    """DOE2 Properties for Dragonfly Story.

    Args:
        host: A dragonfly_core Story object that hosts these properties.

    Properties:
        * host
    """

    __slots__ = ('_host',)

    def __init__(self, host):
        """Initialize Story DOE2 properties."""
        self._host = host

    @property
    def host(self):
        """Get the Story object hosting these properties."""
        return self._host

    @classmethod
    def from_dict(cls, data, host):
        """Create StoryDOE2Properties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of StoryDOE2Properties.
            host: A Story object that hosts these properties.
        """
        assert data['type'] == 'StoryDOE2Properties', \
            'Expected StoryDOE2Properties. Got {}.'.format(data['type'])
        new_prop = cls(host)
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a StoryDOE2PropertiesAbridged dictionary.

        Args:
            abridged_data: A StoryDOE2PropertiesAbridged dictionary (typically
                coming from a Model).
        """
        pass  # currently no properties to apply

    def to_dict(self, abridged=False):
        """Return Story DOE2 properties as a dictionary.

        Args:
            abridged: Boolean for whether the full dictionary of the Story should
                be written (False) or just the identifier of the the individual
                properties (True). Default: False.
        """
        base = {'doe2': {}}
        base['doe2']['type'] = 'StoryDOE2Properties' if not \
            abridged else 'StoryDOE2PropertiesAbridged'
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new Story object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return StoryDOE2Properties(_host)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Story DOE2 Properties: {}'.format(self.host.identifier)
