""" Templates for 'Block Inputs' that are of relative
    Redundance between rooms and story objects
"""
from ..geometry import Vertices
import dragonfly
from dragonfly.room2d import Room2D as df_room
from dragonfly.story import Story as df_story
from .data_classing import IpyDataClass as ipydata


class PolyInput(ipydata):
    df_obj = None

    def __init__(self):
        super(RoomPolyInput, self).__init__()

    def get_verts(obj):
        if type(obj) == df_room:
            flr_vrt_objs = Vertices.from_rm2d(obj)
        elif type(obj) == df_story:
            flr_vrt_objs = Vertices().from_story(obj)
        for obj in flr_vrt_objs:
            data = '\n  '.join('V{obji}               = ( {objx}, {objy} )'.format(
                obji=obj[0], objx=obj[1], objy=obj[2]
            ))
        return data

    def to_inp(self):
        """Return Space/Room Polygons block input"""
        return '"{disp_name} Plg" = POLYGON\n  '.format(
            disp_name=self.df_obj.display_name) + self.get_verts(
            self.df_obj)

    def __repr__(self):
        return self.to_inp()
