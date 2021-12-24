from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from honeybee.boundarycondition import Outdoors
import dragonfly_energy
from dragonfly.model import Model
from dragonfly.story import Story
from dragonfly.room2d import Room2D
import dragonfly
import dragonfly_doe2.inp_blocks as fb
from .hvac import HVAC

###############       ###########
# To Be Replaced Soon ###########
###############       ###########


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
        return self._hvac_zone_data(self.host)

    @staticmethod
    def _hvac_zone_data(hvc_hst):

        spc_hvac = '"Zn ({})" = ZONE\n   '.format(hvc_hst.display_name) + \
            'TYPE           = UNCONDITIONED\n   ' \
            'DESIGN-HEAT-T  = 72\n   '\
            'DESIGN-COOL-T  = 75\n   '\
            'SPACE          ="Spc {}"\n  ..\n'.format(hvc_hst.display_name)
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
            doe_rm = INPRoom(room)
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

    @property
    def hvac_block(self):
        return self._get_hvac_block(self.rooms_doe2)

    @staticmethod
    def _get_hvac_block(doe_rms):
        hvac_data = '\n'.join(rm.hvac_zone_data for rm in doe_rms)
        return(hvac_data)


class INPModel():
    __slots__ = ('_host_model')

    def __init__(self, host_model):
        self._host_model = host_model

    @property
    def host(self):
        return self._host_model

    @property
    def file_start(self):
        return self._make_file_start()

    @staticmethod
    def _make_file_start(_objs=None):
        # TODO:  Make this not hard coded
        block = fb.topLevel+fb.abortDiag+fb.globalParam+fb.ttrpddh + \
            'TITLE\n  LINE-1          = *simple_example*\n  ..\n\n' + \
            '"Entire Year" = RUN-PERIOD-PD\n  ' + \
            'BEGIN-MONTH     = 1\n  ' + \
            'BEGIN-DAY      = 1\n  ' + \
            'BEGIN-YEAR     = 2021\n  ' + \
            'END-MONTH      = 12\n  ' + \
            'END-DAY        = 31\n  ' + \
            'END-YEAR       = 2021\n  ..\n\n' + \
            '"Standard US Holidays" = HOLIDAYS\n  ' + \
            'LIBRARY-ENTRY "US"\n  ..\n\n'
        return(block)

    @property
    def compliance_data(self):
        return self._make_comply(self.host)

    @staticmethod
    def _make_comply(host, _objs=None):
        block = fb.comply + \
            '\n"Compliance Data" = COMPLIANCE\n  ' + \
            'C-PERMIT-SCOPE  = 0\n  ' +\
            'C-PROJ-NAME     = *{}*\n  '.format(host.display_name) +\
            'C-BUILDING-TYPE = 0\n  ' +\
            'C-CONS-PHASE    = 0\n  ' +\
            'C-NR-DHW-INCL   = 0\n  ' +\
            'C-CODE-VERSION  = 1\n  ' +\
            'C-901-NUM-FLRS  = 1\n  ' +\
            'C-901-BLDG-TYPE = 32\n  ..\n\n'
        return(block)

    @property
    def site_bldg_data(self):
        return self._make_site_bldg()

    @staticmethod
    def _make_site_bldg(_objs=None):
        block = fb.siteBldg +\
            '"Site Data" = SITE-PARAMETERS\n  ' +\
            'ALTITUDE          = 150\n  ' +\
            'C-STATE           = 21\n  ' +\
            'C-WEATHER-FILE    = *TMY2\HARTFOCT.bin*\n  ' +\
            'C-COUNTRY         = 1\n  ' +\
            'C-901-LOCATION    = 1092\n  ..\n' +\
            '"Building Data" = BUILD-PARAMETERS\n  ' +\
            'HOLIDAYS        = "Standard US Holidays"\n  ..\n\n\n' +\
            'PROJECT-DATA\n  ..\n\n'
        return(block)

    @property
    def mat_layer_const(self):
        # TODO MLC converion in general needs to be attended to
        return self._mcl_make()

    @staticmethod
    def _mcl_make(_objs=None):
        block = fb.matslayers + \
            '"EWall Cons Mat 2 (5.5)" = MATERIAL\n  ' +\
            'TYPE             = RESISTANCE\n  ..\n' +\
            '"EWall Cons Layers" = LAYERS\n  ' +\
            'MATERIAL          = ("Plywd 5/8in (PW04)", "Insul Bd 1/2in (IN61)",\n  ' +\
            '                     "EWall Cons Mat 2 (5.5)", "GypBd 1/2in (GP01)" )\n  ..\n' +\
            '"EWall Construction" = CONSTRUCTION\n  ' +\
            'TYPE             = LAYERS\n  ' +\
            'ABSORPTANCE      = 0.6\n  ' +\
            'ROUGHNESS        = 4\n  ' +\
            'LAYERS           = "EWall Cons Layers"\n  ..\n\n'
        return(block)

    @property
    def poly_block_data(self):
        return self._make_poly_block_data(self.host)

    @staticmethod
    def _make_poly_block_data(_hst_model):
        ply_strs = []
        for story in _hst_model.stories:
            to_parse = INPStory(story)
            ply_strs.append(to_parse.poly_block)
        block = '\n'.join(obj for obj in ply_strs[0:])
        header = fb.polygons + block
        return(header)

    @property
    def space_block_data(self):
        return self._make_space_block_data(self.host)

    @staticmethod
    def _make_space_block_data(_hst_model):
        spc_strs = []
        for story in _hst_model.stories:
            to_parse = INPStory(story)
            spc_strs.append(to_parse.space_block)
        block = '\n'.join(obj for obj in spc_strs[0:])
        header = fb.floorNspace + block
        return(header)

    @property
    def hvac_block_data(self):
        return self._make_hvac(self.host)

    @staticmethod
    def _make_hvac(hvc_hst):
        hvc_block = fb.hvacSysNzone + HVAC().to_inp_string()
        zn_strs = []
        for story in hvc_hst.stories:
            to_parse = INPStory(story)
            zn_strs.append(to_parse.hvac_block)
        block = '\n'.join(obj for obj in zn_strs[0:])
        header = hvc_block+block
        return(header)

    def to_inp(self):
        # TODO: Dont forget glass
         = self.file_start + self.compliance_data + self.site_bldg_data + \
            self.mat_layer_const + fb.glzCode + fb.glzTyp + fb.WindowLayers + fb.iLikeLamp + \
            fb.daySch + fb.weekSch + fb.annualSch + self.poly_block_data + fb.wallParams + \
            fb.fixBldgShade + fb.miscCost + fb.perfCurve + self.space_block_data + \
            fb.elecFuelMeter + fb.elecMeter + fb.fuelMeter + fb.masterMeter + fb.hvacCircLoop + \
            fb.pumps + fb.heatExch + fb.circLoop + fb.chillyboi + fb.boilyboi + fb.dwh + \
            fb.heatReject + fb.towerFree + fb.pvmod + fb.elecgen + fb.thermalStore + \
            fb.groundLoopHx + fb.compDhwRes + fb.steamAndcldMtr + fb.steamMtr + \
            fb.chillMeter + self.hvac_block_data + fb.miscNmeterHvac + fb.equipControls + \
            fb.loadManage + fb.UtilRate + fb.ratchets + fb.blockCharge + fb.utilRate + fb.outputReporting + \
            fb.loadsNonHr + fb.sysNonHr + fb.plntNonHr + fb.econNonHr + fb.hourlyRep + fb.theEnd

        return()
