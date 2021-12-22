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

    def __init__(self, _host_obj):
        self.host_obj = _host_obj

    @property
    def host(self):
        return self.host_obj

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

    def to_inp_string(self, host_obj):
        if self.object_type == 'Room':
            return(RoomPolyInput(host_obj))
        elif self.object_type == 'Story':
            return(StoryPolyInput(host_obj))

    def __repr__(self):
        return self.to_inp_string(self.host)
