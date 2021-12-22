""" Templates for 'Block Inputs' that are of relative
    Redundance between rooms and story objects
"""
from dataclasses import dataclass
from .doe_geometry import DoeVerts
import dragonfly
from dragonfly.room2d import Room2D as df_room


@dataclass
class RoomPolyInput:
    df_obj: df_room = None

    def get_verts(obj):
        flr_vrt_objs = DoeVerts.from_rm2d(obj)
        for obj in flr_vrt_objs:
            data = '\n  '.join(f'V{obj[0]}               = ( {obj[1]}, {obj[2]}')
        return(data)

    def to_inp(self) -> str:
        """Return Space/Room Polygons block input"""
        return '"{self.df_obj.display_name} plg" = POLYGON\n  ' +\
               self.get_verts(self.df_obj)

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class StoryPolyInput:
    pass
