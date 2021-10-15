"""Some cls for LBT to DOE2 format to keep properties classes clean"""
from ladybug_geometry.geometry3d.face import upper_left_counter_clockwise_vertices as cc_verts

class DoeRoomVerts(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.i = 0
    
    @classmethod
    def from_rm2d(cls, _rm):
        obj = cls
        
        flr_geom = _rm.floor_geometry
        flrvrts = flr_geom.upper_left_counter_clockwise_vertices
        
        doe2_vert_objs = []
        for i, vert in enumerate(flrvrts):
            doe2_vert_objs.append((i+1, vert.x, vert.y))
        
        obj = doe2_vert_objs
        return(obj)

    def __repr__(self):
        return(obj)
        
        
        