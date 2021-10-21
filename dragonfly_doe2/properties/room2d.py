# coding=utf-8
"""Room2D DOE2 Properties."""
from dragonfly.room2d import Room2D
from dragonfly.windowparameter import SimpleWindowRatio
from ladybug_geometry.geometry3d.pointvector import Point3D

#from ..doe_geometry import DoeVertsFromLBT as doe_verts


class Room2DDOE2Properties(object):
    """DOE2 Properties for Dragonfly Room2D.

    Args:
        host: A dragonfly_core Room2D object that hosts these properties.

    Properties:
        * host
        * poly_verts
        * doe_space_poly
    """

    __slots__ = ('_host',)

    def __init__(self, host):
        """Initialize Room2D DOE2 properties."""
        self._host = host

    @property
    def host(self):
        """Get the Room2D object hosting these properties."""
        return self._host

    @property
    def poly_verts(self):
        """Get the Room2D Polygon Vertices."""
        return(self._get_doe_verts(self.host))

    @staticmethod
    def _get_doe_verts(host):
        flr_geom = host.floor_geometry
        flr_verts = flr_geom.upper_left_counter_clockwise_vertices

        doe_verts = []
        for i, vert in enumerate(flr_verts):
            doe_verts.append((i+1, vert.x, vert.y))
        obj = doe_verts
        return(obj)

    @property
    def doe_space_poly(self):
        """ DOE2 Formatted Zone Polygon Object """
        return(_make_doe_spc_ply(self.poly_verts))

    @staticmethod
    def _make_doe_spc_ply(_obj):
        header = '"{} Plg" = POLYGON\n   '.format(room2d.display_name)
        vert_strs = []

        for obj in room2d.Room2DDOE2Properties.poly_verts:
            vstr = 'V{}'.format(obj[0])+(' '*15) + \
                '= ( {} , {} )\n   '.format(obj[1], obj[2])
            vert_strs.append(vstr)

        for obj in vert_strs:
            header = header + obj

    @classmethod
    def from_dict(cls, data, host):
        """Create Room2DDOE2Properties from a dictionary.

        Note that the dictionary must be a non-abridged version for this
        classmethod to work.

        Args:
            data: A dictionary representation of Room2DDOE2Properties.
            host: A Room2D object that hosts these properties.
        """
        assert data['type'] == 'Room2DDOE2Properties', \
            'Expected Room2DDOE2Properties. Got {}.'.format(data['type'])
        new_prop = cls(host)
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        """Apply properties from a Room2DDOE2PropertiesAbridged dictionary.

        Args:
            abridged_data: A Room2DDOE2PropertiesAbridged dictionary (typically
                coming from a Model).
        """
        pass  # currently no properties to apply

    def to_dict(self, abridged=False):
        """Return Room2D DOE2 properties as a dictionary.

        Args:
            abridged: Boolean for whether the full dictionary of the Room2D should
                be written (False) or just the identifier of the the individual
                properties (True). Default: False.
        """
        base = {'doe2': {}}
        base['doe2']['type'] = 'Room2DDOE2Properties' if not \
            abridged else 'Room2DDOE2PropertiesAbridged'
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new Room2D object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return Room2DDOE2Properties(_host)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Room2D DOE2 Properties: {}'.format(self.host.identifier)
