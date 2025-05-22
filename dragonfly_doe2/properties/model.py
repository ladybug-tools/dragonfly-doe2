# coding=utf-8
"""Model DOE-2 Properties."""


class ModelDoe2Properties(object):
    """DOE-2 Properties for Dragonfly Model.

    Args:
        host: A dragonfly_core Model object that hosts these properties.

    Properties:
        * host
    """

    def __init__(self, host):
        """Initialize ModelDoe2Properties."""
        self._host = host

    @property
    def host(self):
        """Get the Model object hosting these properties."""
        return self._host

    def check_for_extension(self, raise_exception=True, detailed=False):
        """Check that the Model is valid for DOE-2 simulation.

        This process includes all relevant dragonfly-core checks as well as checks
        that apply only for DOE-2.

        Args:
            raise_exception: Boolean to note whether a ValueError should be raised
                if any errors are found. If False, this method will simply
                return a text string with all errors that were found. (Default: True).
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A text string with all errors that were found or a list if detailed is True.
            This string (or list) will be empty if no errors were found.
        """
        # set up defaults to ensure the method runs correctly
        detailed = False if raise_exception else detailed
        msgs = []
        tol = self.host.tolerance
        ang_tol = self.host.angle_tolerance

        # perform checks for duplicate identifiers, which might mess with other checks
        msgs.append(self.host.check_all_duplicate_identifiers(False, detailed))

        # perform checks for key dragonfly model schema rules
        msgs.append(self.host.check_degenerate_room_2ds(tol, False, detailed))
        msgs.append(self.host.check_self_intersecting_room_2ds(tol, False, detailed))
        msgs.append(self.host.check_plenum_depths(tol, False, detailed))
        msgs.append(self.host.check_window_parameters_valid(tol, False, detailed))
        msgs.append(self.host.check_no_room2d_overlaps(tol, False, detailed))
        msgs.append(self.host.check_collisions_between_stories(tol, False, detailed))
        msgs.append(self.host.check_roofs_above_rooms(tol, False, detailed))
        msgs.append(self.host.check_room2d_floor_heights_valid(False, detailed))
        msgs.append(self.host.check_missing_adjacencies(False, detailed))
        msgs.append(self.host.check_all_room3d(tol, ang_tol, False, detailed))

        # perform checks that are specific to DOE-2
        msgs.append(self.check_all_zones_have_one_hvac(False, detailed))
        msgs.append(self.check_maximum_elevation(1000, False, detailed))

        # output a final report of errors or raise an exception
        full_msgs = [msg for msg in msgs if msg]
        if detailed:
            return [m for msg in full_msgs for m in msg]
        full_msg = '\n'.join(full_msgs)
        if raise_exception and len(full_msgs) != 0:
            raise ValueError(full_msg)
        return full_msg

    def to_dict(self):
        """Return Model DOE-2 properties as a dictionary."""
        return {'doe2': {'type': 'ModelDoe2Properties'}}

    def apply_properties_from_dict(self, data):
        """Apply the energy properties of a dictionary to the host Model of this object.

        Args:
            data: A dictionary representation of an entire dragonfly-core Model.
                Note that this dictionary must have ModelEnergyProperties in order
                for this method to successfully apply the energy properties.
        """
        assert 'doe2' in data['properties'], \
            'Dictionary possesses no ModelDoe2Properties.'
        room_doe2_dicts = []
        if 'buildings' in data and data['buildings'] is not None:
            for b_dict in data['buildings']:
                if 'unique_stories' in b_dict and b_dict['unique_stories'] is not None:
                    for story_dict in b_dict['unique_stories']:
                        for room_dict in story_dict['room_2ds']:
                            try:
                                room_doe2_dicts.append(room_dict['properties']['doe2'])
                            except KeyError:
                                room_doe2_dicts.append(None)
        if len(room_doe2_dicts) != 0:
            for room, r_dict in zip(self.host.room_2ds, room_doe2_dicts):
                if r_dict is not None:
                    room.properties.doe2.apply_properties_from_dict(r_dict)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Model DOE2 Properties: [host: {}]'.format(self.host.display_name)
