""" Templates for 'Block Inputs' that are of relative
    Redundance between rooms and story objects
"""
from dragonfly.room2d import Room2D
from dragonfly.story import Story


class Polygon(object):
    "A Doe2 Polygon."
    def __init__(self, name, vertices):
        self.name = name
        self.vertice = vertices

    @classmethod
    def from_room(cls, room: Room2D, tolerace=0.01):
        """
        Note: Shouldn't we ensure the points are in 2D. I'm not sure how it works.
        """
        cf = room.floor_geometry.remove_colinear_vertices(tolerance=tolerace)
        vertices = cf.upper_left_counter_clockwise_vertices
        return cls(room.display_name, vertices)
    
    @classmethod
    def from_story(cls, story: Story, tolerace=0.01):
        """
        Note: I'm not sure if this is correct - shouldn't we create a polygon per face?
        This is based on the initial code by Trevor so I didn't change it.
        """
        geo = story.footprint(tolerance=tolerace)
        vertices = []
        for face in geo:
            cf = face.remove_colinear_vertices(tolerance=tolerace)
            vertices.extend(cf.upper_left_counter_clockwise_vertices)
        return cls(story.display_name, vertices)

    def to_inp(self) -> str:
        """Return Room Polygons block input"""
        vertices_template = '   V%d\t\t= ( %f, %f )'.replace('\t', '    ')
        vertices = '\n'.join([
            vertices_template % (i + 1, ver.x, ver.y)
            for i, ver in enumerate(self.vertice)
        ])
        return f'"{self.name} Polygon" = POLYGON\n' \
               f'{vertices}\n' + \
               '   ..'

    def __repr__(self):
        return self.to_inp()
