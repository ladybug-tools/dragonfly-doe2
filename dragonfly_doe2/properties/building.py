# coding=utf-8
"""Building DOE2 Properties."""
from __future__ import division


class BuildingDOE2Properties(object):
    """DOE2 Properties for Dragonfly Building.

    Args:
        host: A dragonfly_core Building object that hosts these properties.

    Properties:
        * host
    """
    __slots__ = ('_host',)

    def __init__(self, host):
        """Initialize Building DOE2 properties."""
        self._host = host

    @property
    def host(self):
        """Get the Building object hosting these properties."""
        return self._host

    @classmethod
    def from_dict(cls, data, host):
        """Create BuildingDOE2Properties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of BuildingDOE2Properties.
            host: A Building object that hosts these properties.
        """
        assert data['type'] == 'BuildingDOE2Properties', \
            'Expected BuildingDOE2Properties. Got {}.'.format(data['type'])
        return cls(host)

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a BuildingDOE2PropertiesAbridged dictionary.

        Args:
            abridged_data: A BuildingDOE2PropertiesAbridged dictionary (typically
                coming from a Model).
        """
        pass

    def to_dict(self, abridged=False):
        """Return Building DOE2 properties as a dictionary.

        Args:
            abridged: Boolean for whether the full dictionary of the Building should
                be written (False) or just the identifier of the the individual
                properties (True). Default: False.
        """
        base = {'doe2': {}}
        base['doe2']['type'] = 'BuildingDOE2Properties' if not \
            abridged else 'BuildingDOE2PropertiesAbridged'
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new Building object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        _new_obj = BuildingDOE2Properties(_host)
        return _new_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Building DOE2 Properties: {}'.format(self.host.identifier)
