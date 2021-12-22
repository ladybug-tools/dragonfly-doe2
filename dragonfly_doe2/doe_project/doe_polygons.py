from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from honeybee.boundarycondition import Outdoors
import dragonfly_energy
from dragonfly.room2d import Room2D
from dragonfly.story import Story
import dragonfly
import dragonfly_doe2.inp_file.fileblocks as fb
from .doe_hvac import DoeHVAC
from .doe_geometry import DoeVerts
from .doe_templates import RoomPolyInput


class DOEPoly(object):
    """ An agnostic DOE poly block Object for rooms and stories """
    __slots__ = ('_host_object')

    def __init__(self, host_object):
        self._host_object = host_object

    @property
    def host(self):
        return self._host_object

    @property
    def object_type(self):
        return self._object_type(self.host)

    @staticmethod
    def _object_type(obj_to_type):
        if obj_type:
            if type(obj_to_type) == 'dragonfly.story.Story':
                rtrn_type = 'Story'
            elif type(obj_to_type) == 'dragonfly.room2d.Room2D':
                rtrn_type = 'Room'
        return(rtrn_type)
