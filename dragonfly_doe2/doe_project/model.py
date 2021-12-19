from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
import dragonfly_energy
from hvac import DoeHVAC


class Model(Story):
    __slots__ = ()


class Story(Room):
    __slots__ = ('_host')

    def __init__(self, host):
        self.host = host

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, hst):
        self._host = hst


class Room(object):
    __slots__ = ('_host', '_poly_data', '_space_data', '_hvac_zone_data')

    def __init__(self, host):
        self.host = host

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, hst):
        self._host = hst

    @property
    def poly_data(self):
        return self._poly_data

    @poly_data.setter
    def poly_data(self, ply_hst):
        if ply_hst is not None:
            flr_geom = host.floor_geometry
            flr_verts = flr_geom.upper_left_counter_clockwise_vertices

            doe_verts = []
            for i, vert in enumerate(flr_verts):
                doe_verts.append((i+1, vert.x, vert.y))
            poly_verts = doe_verts

            assert isinstance(ply_hst, dragonfly.room2d.Room2D), 'Expected DF Room2d' \
                'got:{}'.format(type(ply_hst))
            header = '"{} Plg" = POLYGON\n   '.format(ply_hst.display_name)
            vert_strs = []
            for obj in poly_verts:
                vstr = 'V{}'.format(obj[0])+(' '*15) + \
                    '= ( {} , {} )\n   '.format(obj[1], obj[2])
                vert_strs.append(vstr)

            for obj in vert_strs:
                header = header + obj
        self._poly_data = header

    @property
    def space_data(self):
        return self._space_data

    @space_data.setter
    def space_data(self, spc_hst):
        if spc_hst is not None:
            assert isinstance(spc_hst, dragonfly.room2d.Room2D), 'Expected DF Room2D' \
                'Got:{}'.format(type(spc_hst))

            header = '"{}" = SPACE\n   SHAPE'.format(spc_hst.display_name) +\
                ' '*12+'= POLYGON\n   '+'POLYGON'+' '*10 + \
                '= "{} Plg"\n   '.format(spc_hst.display_name) + \
                'C-ACTIVITY-DESC  = *{}*\n   ..'.format(
                spc_hst.properties.energy.program_type.display_name)

        self._space_data = header
# TODO: Need to factor in walls

    @property
    def hvac_zone_data(self):
        return self._hvac_zone_data

    @hvac_zone_data.setter
    def hvac_zone_data(self, hvc_hst):
        if hvc_hst is not None:
            assert isinstance(hvc_hst, dragonfly.room2d.Room2D), 'Expected DF Room2D' \
                'Got: {}'.format(type(hvc_hst))
            spc_hvac = '"Zn ({})" = ZONE\n   '.format(hvc_hst.display_name) + \
                'TYPE           = UNCONDITIONED\n   ' \
                'DESIGN-HEAT-T  = 72\n   '\
                'DESIGN-COOL-T  = 75\n   '\
                'SPACE          ="Spc {}"'.format(hvc_hst.display_name)
            self._hvac_zone_data = spc_hvac


def poly_str(_df_obj):
    """ Takes a Dragonfly Object and creates a
        DOE2 *.inp input 'polygon object

        Args:
            _df_obj: df_room2d or df_story objects.

        Returns:
        *inp string:
        .. code-block:: f#

            "Ground_Office1 Plg" = POLYGON
                V1               = ( 0.0 , 0.0 )
                V2               = ( 10.0 , 0.0 )
                V3               = ( 10.0 , 10.0 )
                V4               = ( 0.0 , 10.0 )
    """
    if isinstance(_df_obj, dragonfly.room2d.Room2D):
        header = '"{} Plg" = POLYGON\n   '.format(_df_obj.display_name)
        vert_strs = []
        for obj in _df_obj.properties.doe2.poly_verts:
            vstr = 'V{}'.format(obj[0])+(' '*15) + \
                '= ( {} , {} )\n   '.format(obj[1], obj[2])
            vert_strs.append(vstr)

        for obj in vert_strs:
            header = header + obj
        return(header)

    elif isinstance(_df_obj, dragonfly.story.Story):
        header = '"{} Floor Plg" = POLYGON\n   '.format(_df_obj.display_name)
        vert_strs = []
        for obj in _df_obj.properties.doe2.story_poly_verts:
            vstr = 'V{}'.format(obj[0])+(' '*15) + \
                '= ( {} , {} )\n   '.format(obj[1], obj[2])
            vert_strs.append(vstr)

        for obj in vert_strs:
            header = header + obj

        return(header)


def doe_spc(_df_obj):
    if isinstance(_df_obj, dragonfly.room2d.Room2D):
        header = '"{}" = SPACE\n   SHAPE'.format(_df_obj.display_name) +\
            ' '*12+'= POLYGON\n   '+'POLYGON'+' '*10 + \
            '= "{} Plg"\n   '.format(_df_obj.display_name) + \
            'C-ACTIVITY-DESC  = *{}*\n   ..'.format(
                _df_obj.properties.energy.program_type.display_name)

        return(header)

    elif isinstance(_df_obj, dragonfly.story.Story):
        header = '"{}" = FLOOR\n   Z'.format(_df_obj.display_name) + \
            ' '*16+'= {}\n   '.format(_df_obj.floor_height) + \
            'POLYGON'+' '*10+'= "{} Floor Plg"\n   '.format(_df_obj.display_name) + \
            'SHAPE'+' '*12+'= POLYGON\n   ' + \
            'FLOOR-HEIGHT     = {}\n   '.format(_df_obj.floor_to_floor_height) + \
            'C-DIAGRAM-DATA   = *{} UI DiagData*\n   ..'.format(
                _df_obj.display_name)

        return(header)
