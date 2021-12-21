from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from honeybee.boundarycondition import Outdoors
import dragonfly_energy
from .hvac import DoeHVAC
from dragonfly.room2d import Room2D
import dragonfly

# class INPModel(Story):
#__slots__ = ()


class INPRoom():
    __slots__ = ('_host_room')

    def __init__(self, host_room):
        self._host_room = host_room

    @property
    def host(self):
        return self._host_room

    @property
    def poly_data(self):
        return self._poly_data(self.host)

    @staticmethod
    def _poly_data(ply_hst):
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
        if ply_hst is not None:
            flr_geom = ply_hst.floor_geometry
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
            header += '..\n'
        return(header)

    @property
    def space_data(self):
        return self._space_data(self.host)

    @staticmethod
    def _space_data(spc_hst):
        if spc_hst is not None:
            assert isinstance(spc_hst, dragonfly.room2d.Room2D), 'Expected DF Room2D' \
                'Got:{}'.format(type(spc_hst))

            header = '"{}" = SPACE\n   SHAPE'.format(spc_hst.display_name) +\
                ' '*12+'= POLYGON\n   '+'POLYGON'+' '*10 + \
                '= "{} Plg"\n   '.format(spc_hst.display_name) + \
                'C-ACTIVITY-DESC  = *{}*\n   ..\n'.format(
                spc_hst.properties.energy.program_type.display_name)

            wall_find = []
            bcs = [str(bc) for bc in spc_hst.boundary_conditions]
            for i, bc in enumerate(bcs):
                if bc == 'Outdoors':
                    wall_str = '"{} Wall_{}" = EXTERIOR-WALL\n  '.format(
                        spc_hst.display_name, i + 1) + \
                        'CONSTRUCTION    = "EWall Construction"\n  ' + \
                        'LOCATION        = SPACE-V{}\n   ..'.format(i+1)
                    wall_find.append(wall_str)

            wall_data = '\n'.join(obj for obj in wall_find[0:])
            header = header + wall_data

        return(header)

    @property
    def hvac_zone_data(self):
        return self._hvac_zone_data

    @staticmethod
    def hvac_zone_data(hvc_hst):
        if hvc_hst is not None:
            assert isinstance(hvc_hst, dragonfly.room2d.Room2D), 'Expected DF Room2D' \
                'Got: {}'.format(type(hvc_hst))
            spc_hvac = '"Zn ({})" = ZONE\n   '.format(hvc_hst.display_name) + \
                'TYPE           = UNCONDITIONED\n   ' \
                'DESIGN-HEAT-T  = 72\n   '\
                'DESIGN-COOL-T  = 75\n   '\
                'SPACE          ="Spc {}"'.format(hvc_hst.display_name)
            return(spc_hvac)


class INPStory():
    __slots__ = ('_host_story')

    def __init__(self, host_story):
        self._host_story = host_story

    @property
    def host(self):
        return self._host_story

    @property
    def rooms_doe2(self):
        return(self._make_doe_rooms(self.host))

    @staticmethod
    def _make_doe_rooms(obj):
        doe_rms = []
        for room in obj.room_2ds:
            doe_rm = Room(room)
            doe_rms.append(doe_rm)
        return(doe_rms)

    @property
    def poly_data(self):
        return self._poly_data(self.host)

    @staticmethod
    def _poly_data(ply_hst):
        assert isinstance(ply_hst, dragonfly.story.Story), 'Expected DF Story' \
            'Got: {}'.format(type(ply_hst))
        temp_geom = ply_hst.duplicate().footprint()
        doe_verts = []
        for face in temp_geom:
            cleanface = face.remove_colinear_vertices(0.01)
            for i, vert in enumerate(cleanface.upper_left_counter_clockwise_vertices):
                doe_verts.append((i+1, vert.x, vert.y))

        header = '"{} Floor Plg" = POLYGON\n   '.format(ply_hst.display_name)
        vert_strs = []
        for obj in doe_verts:
            vstr = 'V{}'.format(obj[0])+(' '*15) + \
                '= ( {} , {} )\n   '.format(obj[1], obj[2])
            vert_strs.append(vstr)

        for obj in vert_strs:
            header = header + obj
        header += '..\n'
        return(header)

    @property
    def poly_block(self):
        return self._poly_block(self.rooms_doe2, self.poly_data)

    @staticmethod
    def _poly_block(doe_rms, plydta):

        story_poly_block = plydta
        roomstrs = '\n'.join(rm.poly_data for rm in doe_rms[0:])
        ply_block = story_poly_block + roomstrs
        return(ply_block)

    @property
    def space_data(self):
        return self._space_data(self.host)

    @staticmethod
    def _space_data(spc_hst):
        assert isinstance(spc_hst, dragonfly.story.Story), 'Expected DF Story' \
            'Got: {}'.format(type(spc_hst))
        header = '"{}" = FLOOR\n   Z'.format(spc_hst.display_name) + \
            ' '*16+'= {}\n   '.format(spc_hst.floor_height) + \
            'POLYGON'+' '*10+'= "{} Floor Plg"\n   '.format(spc_hst.display_name) + \
            'SHAPE'+' '*12+'= POLYGON\n   ' + \
            'FLOOR-HEIGHT     = {}\n   '.format(spc_hst.floor_to_floor_height) + \
            'C-DIAGRAM-DATA   = *{} UI DiagData*\n   ..\n'.format(
                spc_hst.display_name)
        return(header)

    @property
    def space_block(self):
        return self._space_block(self.rooms_doe2, self.space_data)

    @staticmethod
    def _space_block(doe_rms, spcdta):
        story_spc_block = spcdta
        roomstrs = '\n'.join(rm.space_data for rm in doe_rms[0:])
        spc_block = story_spc_block + roomstrs
        return(spc_block)
