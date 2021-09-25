# coding=utf-8
"""Context Shade DOE2 Properties."""


class ContextShadeDOE2Properties(object):
    """DOE2 Properties for Dragonfly ContextShade.

    Args:
        host_shade: A dragonfly_core ContextShade object that hosts these properties.

    Properties:
        * host
    """

    __slots__ = ('_host',)

    def __init__(self, host_shade, is_vegetation=False):
        """Initialize ContextShade DOE2 properties."""
        self._host = host_shade

    @property
    def host(self):
        """Get the Shade object hosting these properties."""
        return self._host

    @classmethod
    def from_dict(cls, data, host):
        """Create ContextShadeDOE2Properties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of ContextShadeDOE2Properties.
            host: A ContextShade object that hosts these properties.
        """
        assert data['type'] == 'ContextShadeDOE2Properties', \
            'Expected ContextShadeDOE2Properties. Got {}.'.format(data['type'])
        return cls(host)

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a ContextShadeDOE2PropertiesAbridged dictionary.

        Args:
            abridged_data: A ContextShadeDOE2PropertiesAbridged dictionary (typically
                coming from a Model).
        """
        pass

    def to_dict(self, abridged=False):
        """Return DOE2 properties as a dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
        """
        base = {'doe2': {}}
        base['doe2']['type'] = 'ContextShadeDOE2Properties' if not \
            abridged else 'ContextShadeDOE2PropertiesAbridged'
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new ContextShade object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return ContextShadeDOE2Properties(_host)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Context Shade DOE2 Properties: {}'.format(self.host.identifier)
