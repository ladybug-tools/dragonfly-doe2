# coding=utf-8
"""Room2D DOE-2 Properties."""
from honeybee.typing import float_in_range, float_positive
from honeybee.altnumber import autocalculate
from honeybee_doe2.properties.room import RoomDoe2Properties


class Room2DDoe2Properties(object):
    """DOE-2 Properties for Dragonfly Room2D.

    Args:
        host: A dragonfly_core Room2D object that hosts these properties.
        assigned_flow: A number for the design supply air flow rate for the zone
            the Room2D is assigned to (cfm). This establishes the minimum allowed
            design air flow. Note that the actual design flow may be larger. If
            None, this parameter will not be written into the INP. (Default: None).
        flow_per_area: A number for the design supply air flow rate to
            the zone per unit floor area (cfm/ft2). If None, this parameter
            will not be written into the INP. (Default: None).
        min_flow_ratio: A number between 0 and 1 for the minimum allowable zone
            air supply flow rate, expressed as a fraction of design flow rate.
            Applicable to variable-volume type systems only. If None, this parameter
            will not be written into the INP. (Default: None).
        min_flow_per_area: A number for the minimum air flow per square foot of
            floor area (cfm/ft2). This is an alternative way of specifying the
            min_flow_ratio. If None, this parameter will not be written into
            the INP. (Default: None).
        hmax_flow_ratio: A number between 0 and 1 for the ratio of the maximum
            (or fixed) heating airflow to the cooling airflow. The specific
            meaning varies according to the type of zone terminal. If None, this
            parameter will not be written into the INP. (Default: None).

    Properties:
        * host
        * assigned_flow
        * flow_per_area
        * min_flow_ratio
        * min_flow_per_area
        * hmax_flow_ratio
    """
    __slots__ = (
        '_host', '_assigned_flow', '_flow_per_area', '_min_flow_ratio',
        '_min_flow_per_area', '_hmax_flow_ratio',
    )

    def __init__(
        self, host, assigned_flow=None, flow_per_area=None, min_flow_ratio=None,
        min_flow_per_area=None, hmax_flow_ratio=None
    ):
        """Initialize Room2D DOE-2 properties."""
        # set the main properties of the Room2D
        self._host = host
        self.assigned_flow = assigned_flow
        self.flow_per_area = flow_per_area
        self.min_flow_ratio = min_flow_ratio
        self.min_flow_per_area = min_flow_per_area
        self.hmax_flow_ratio = hmax_flow_ratio

    @property
    def host(self):
        """Get the Room2D object hosting these properties."""
        return self._host

    @property
    def assigned_flow(self):
        """Get or set the design supply air flow rate for the zone (cfm)."""
        return self._assigned_flow

    @assigned_flow.setter
    def assigned_flow(self, value):
        if value is not None:
            value = float_positive(value, 'zone assigned flow')
        self._assigned_flow = value

    @property
    def flow_per_area(self):
        """Get or set the design supply air flow rate per unit floor area (cfm/ft2).
        """
        return self._flow_per_area

    @flow_per_area.setter
    def flow_per_area(self, value):
        if value is not None:
            value = float_positive(value, 'zone flow per area')
        self._flow_per_area = value

    @property
    def min_flow_ratio(self):
        """Get or set the the min supply airflow rate as a fraction of design flow rate.
        """
        return self._min_flow_ratio

    @min_flow_ratio.setter
    def min_flow_ratio(self, value):
        if value is not None:
            value = float_in_range(value, 0.0, 1.0, 'zone min flow ratio')
        self._min_flow_ratio = value

    @property
    def min_flow_per_area(self):
        """Get or set the minimum air flow per square foot of floor area (cfm/ft2)."""
        return self._min_flow_per_area

    @min_flow_per_area.setter
    def min_flow_per_area(self, value):
        if value is not None:
            value = float_positive(value, 'zone min flow per area')
        self._min_flow_per_area = value

    @property
    def hmax_flow_ratio(self):
        """Get or set the ratio of the maximum heating airflow to the cooling airflow.
        """
        return self._hmax_flow_ratio

    @hmax_flow_ratio.setter
    def hmax_flow_ratio(self, value):
        if value is not None:
            value = float_in_range(value, 0.0, 1.0, 'zone heating max flow ratio')
        self._hmax_flow_ratio = value

    def check_floor_plate_vertex_count(self, raise_exception=True, detailed=False):
        """Check whether the Room2D's floor geometry exceeds the maximum vertex count.

        The DOE-2 engine currently does not support such rooms and limits the
        total number of vertices to 120.

        Args:
            raise_exception: If True, a ValueError will be raised if the Room2D
                floor plate exceeds the maximum number of vertices supported by
                DOE-2. (Default: True).
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A string with the message or a list with a dictionary if detailed is True.
        """
        if len(self.host.floor_geometry.boundary) > 120:
            msg = 'Room2D "{}" has a floor plate with {} vertices, which is more ' \
                'than the maximum 120 vertices supported by DOE-2.'.format(
                    self.host.display_name, len(self.host.floor_geometry.boundary))
            if raise_exception:
                raise ValueError(msg)
            full_msg = self.host._validation_message_child(
                msg, self.host, detailed, '030101', extension='DOE2',
                error_type='Room Exceeds Maximum Vertex Count')
            if detailed:
                return [full_msg]
            if raise_exception:
                raise ValueError(full_msg)
            return full_msg
        return [] if detailed else ''

    def check_no_floor_plate_holes(self, raise_exception=True, detailed=False):
        """Check whether the Room2D's floor geometry has holes.

        EQuest currently has no way to represent such rooms so, if the issue
        is not addressed, the hole will simply be removed as part of the
        process of exporting to an INP file.

        Args:
            raise_exception: If True, a ValueError will be raised if the Room2D
                floor plate has one or more holes. (Default: True).
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A string with the message or a list with a dictionary if detailed is True.
        """
        if self.host.floor_geometry.has_holes:
            hole_count = len(self.host.floor_geometry.holes)
            hole_msg = 'a hole' if hole_count == 1 else '{} holes'.format(hole_count)
            msg = 'Room2D "{}" has a floor plate with {}, which the eQuest ' \
                'interface cannot represent.'.format(self.host.display_name, hole_msg)
            if raise_exception:
                raise ValueError(msg)
            full_msg = self.host._validation_message_child(
                msg, self.host, detailed, '030102', extension='DOE2',
                error_type='Room Contains Holes')
            if detailed:
                return [full_msg]
            if raise_exception:
                raise ValueError(full_msg)
            return full_msg
        return [] if detailed else ''

    @classmethod
    def from_dict(cls, data, host):
        """Create Room2DDoe2Properties from a dictionary.

        Args:
            data: A dictionary representation of Room2DDoe2Properties with the
                format below.
            host: A Room2D object that hosts these properties.

        .. code-block:: python

            {
            "type": 'Room2DDoe2Properties',
            "assigned_flow": 100,  # number in cfm
            "flow_per_area": 1,  # number in cfm/ft2
            "min_flow_ratio": 0.3, # number between 0 and 1
            "min_flow_per_area": 0.3, # number in cfm/ft2
            "hmax_flow_ratio": 0.3  # number between 0 and 1
            }
        """
        assert data['type'] == 'Room2DDoe2Properties', \
            'Expected Room2DDoe2Properties. Got {}.'.format(data['type'])
        new_prop = cls(host)
        auto_dict = autocalculate.to_dict()
        if 'assigned_flow' in data and data['assigned_flow'] != auto_dict:
            new_prop.assigned_flow = data['assigned_flow']
        if 'flow_per_area' in data and data['flow_per_area'] != auto_dict:
            new_prop.flow_per_area = data['flow_per_area']
        if 'min_flow_ratio' in data and data['min_flow_ratio'] != auto_dict:
            new_prop.min_flow_ratio = data['min_flow_ratio']
        if 'min_flow_per_area' in data and data['min_flow_per_area'] != auto_dict:
            new_prop.min_flow_per_area = data['min_flow_per_area']
        if 'hmax_flow_ratio' in data and data['hmax_flow_ratio'] != auto_dict:
            new_prop.hmax_flow_ratio = data['hmax_flow_ratio']
        return new_prop

    def apply_properties_from_dict(self, data):
        """Apply properties from a Room2DDoe2Properties dictionary.

        Args:
            data: A Room2DDoe2Properties dictionary (typically coming from a Model).
        """
        auto_dict = autocalculate.to_dict()
        if 'assigned_flow' in data and data['assigned_flow'] != auto_dict:
            self.assigned_flow = data['assigned_flow']
        if 'flow_per_area' in data and data['flow_per_area'] != auto_dict:
            self.flow_per_area = data['flow_per_area']
        if 'min_flow_ratio' in data and data['min_flow_ratio'] != auto_dict:
            self.min_flow_ratio = data['min_flow_ratio']
        if 'min_flow_per_area' in data and data['min_flow_per_area'] != auto_dict:
            self.min_flow_per_area = data['min_flow_per_area']
        if 'hmax_flow_ratio' in data and data['hmax_flow_ratio'] != auto_dict:
            self.hmax_flow_ratio = data['hmax_flow_ratio']

    def to_dict(self, abridged=False):
        """Return Room2D Doe2 properties as a dictionary."""
        base = {'doe2': {}}
        base['doe2']['type'] = 'Room2DDoe2Properties'
        if self.assigned_flow is not None:
            base['doe2']['assigned_flow'] = self.assigned_flow
        if self.flow_per_area is not None:
            base['doe2']['flow_per_area'] = self.flow_per_area
        if self.min_flow_ratio is not None:
            base['doe2']['min_flow_ratio'] = self.min_flow_ratio
        if self.min_flow_per_area is not None:
            base['doe2']['min_flow_per_area'] = self.min_flow_per_area
        if self.hmax_flow_ratio is not None:
            base['doe2']['hmax_flow_ratio'] = self.hmax_flow_ratio
        return base

    def to_honeybee(self, new_host):
        """Get a honeybee version of this object.

        Args:
            new_host: A honeybee-core Room object that will host these properties.
        """
        return RoomDoe2Properties(
            new_host, self.assigned_flow, self.flow_per_area, self.min_flow_ratio,
            self.min_flow_per_area, self.hmax_flow_ratio
        )

    def from_honeybee(self, hb_properties):
        """Transfer Doe-2 attributes from a Honeybee Room to Dragonfly Room2D.

        Args:
            hb_properties: The RoomDoe2Properties of the honeybee Room that is being
                translated to a Dragonfly Room2D.
        """
        self._assigned_flow = hb_properties._assigned_flow
        self._flow_per_area = hb_properties._flow_per_area
        self._min_flow_ratio = hb_properties._min_flow_ratio
        self._min_flow_per_area = hb_properties._min_flow_per_area
        self._hmax_flow_ratio = hb_properties._hmax_flow_ratio

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        Args:
            new_host: A new Room2D object that hosts these properties.
                If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        new_room = Room2DDoe2Properties(
            _host, self.assigned_flow, self.flow_per_area, self.min_flow_ratio,
            self.min_flow_per_area, self.hmax_flow_ratio)
        return new_room

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Room2D DOE2 Properties: [host: {}]'.format(self.host.display_name)
