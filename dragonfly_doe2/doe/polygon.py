""" Templates for 'Block Inputs' that are of relative
    Redundance between rooms and story objects
"""
from dragonfly.room2d import Room2D
from dragonfly.story import Story
from .utils import short_name, lower_left_properties


class Polygon(object):
    "A Doe2 Polygon."

    def __init__(self, name, vertices):
        self.name = name
        self.vertice = vertices

    @classmethod
    def from_room(cls, room: Room2D, tolerace=0.01):
        """
        Note: Shouldn't we ensure the points are in 2D. I'm not sure how it works.
        #TF: ooohhhhhhhhhh good catch!! Though is there not already built into DF something
            of the sort for room.floor_geom? was operating off the *assumption* that obj.prop
            would be good to go as is? or am I misunderstanding the specifics in which should
            do check: raise exception if issue?
        """
        room.remove_duplicate_vertices()
        # TODO: on refactor, need to minimize the disconnect between the poly and 'space' room
        vertices = lower_left_properties(room)[0]
        return cls(room.display_name, vertices)

    @classmethod
    def from_story(cls, story: Story, tolerance=0.01):
        """
        Note: I'm not sure if this is correct - shouldn't we create a polygon per face?
        This is based on the initial code by Trevor so I didn't change it.
        """
        geo = story.footprint(tolerance=tolerance)[0]
        # 
        b_pts = geo.boundary
        # remove duplicate vertices if any
        new_bound = []
        b_pts = b_pts[1:] + (b_pts[0],)
        for i, vert in enumerate(b_pts):
            if not vert.is_equivalent(b_pts[i - 1], tolerance):
                new_bound.append(b_pts[i - 1])
        return cls(story.display_name, new_bound)

    def to_inp(self) -> str:
        """Return Room Polygons block input"""
        vertices_template = '   V%d\t\t= ( %f, %f )'.replace('\t', '    ')
        vertices = '\n'.join([
            vertices_template % (i + 1, ver.x, ver.y)
            for i, ver in enumerate(self.vertice)
        ])
        return f'"{self.name} Plg" = POLYGON\n' \
               f'{vertices}\n' + \
               '   ..'

    def __repr__(self):
        return self.to_inp()
