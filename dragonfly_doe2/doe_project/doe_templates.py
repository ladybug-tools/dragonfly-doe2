""" Templates for 'Block Inputs' that are of relative
    Redundance between rooms and story objects
"""
from dataclasses import dataclass
from .doe_geometry import DoeVerts


@dataclass
class RoomPolyInput:
    obj_name: str = None
    verts: DoeVerts = None

    def to_inp(self) -> str:
        """Return Space/Room Polygons block input"""
        return '"{self.obj_name} plg" = POLYGON\n  ' \
               'V'

    def __repr__(self) -> str:
        return self.to_inp()
