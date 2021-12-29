from dragonfly.room2d import Room2D
from dragonfly.story import Story
from dataclasses import dataclass
from typing import List
from .utils import short_name


@dataclass
class Slab:
    """Object for 'floor' surface.

        Init method(s):
            1. from_room(name, construction, type_adjacency).
            note: temp naming conv: intent is for at space class level to
            check if is_ground_contact == True; do SpaceFloor init.

        Args:
            name: space name. (is joined with _floor_{n}). 
            construction: display_name of the floor's construction
            type_adjacency: for now 'BOTTOM' only.

    Example:
        .. code-block:: f#

            "Flr (G.1.U1)" = UNDERGROUND-WALL
                CONSTRUCTION     = "UFCons (G.1.U2)"
                LOCATION         = BOTTOM
                ..
    """
    name: str
    construction: str
    type_adjacency: str = 'BOTTOM'

    @classmethod
    def from_room(
            cls, name: str, construction: str, type_adjacency: str = 'BOTTOM'):
        return cls(name=name, construction=construction, type_adjacency=type_adjacency)

    def to_inp(self):
        return f'"{self.name}_grnd_flr" = UNDERGROUND-WALL\n' \
               f'   CONSTRUCTION    = "{self.construction}_c"\n' \
               f'   LOCATION        = {self.type_adjacency}\n   ..'

    def __repr__(self):
        return self.to_inp()


@dataclass
class RoofCeiling:
    # TODO: Need to add "what's on the other side" for interior adj ceilings.
    # ! Currently will only provide exterior roof for roofs with no internal adj's
    # ? if not needed full interior detailing: Need to add to solve adj: story<->story solve adj
    """Object for roof/ceiling inputs.

        Init method(s):
            1. from_room(name, construction, type_adjacency, next_to=None)

        Args:
            name: space name. (is joind with _roof_{n}).
            construction: display_name of roof_ceiling's constr.
            next_to: *optional* WIP for interior ceilings adjacent space ID#!WIP
    Example:

        .. code-block:: f#

            "Roof (G.2.E9)" = EXTERIOR-WALL   
                CONSTRUCTION     = "Roof Construction"
                LOCATION         = TOP
                ..
            "Ceiling (G.1.I1)" = INTERIOR-WALL   
                NEXT-TO          = "Plnm (G.2)"
                CONSTRUCTION     = "Ceilg Construction"
                LOCATION         = TOP
                ..
    """
    name: str
    construction: str
    next_to: str = None

    @classmethod
    def from_room(cls, room: Room2D):
        name = room.display_name
        construction = room.properties.energy.construction_set.roof_ceiling_set.exterior_construction.display_name
        return cls(name, construction)

    def to_inp(self):
        return f'"{self.name}_roof" = EXTERIOR-WALL\n' \
               f'   CONSTRUCTION    = "{self.construction}_c"\n' \
               f'   LOCATION        = TOP\n   ..'

    def __repr__(self):
        return self.to_inp()


@dataclass
class Wall:
    """*.inp Wall object.

        Init method(s):
            1. from_room_seg(name, location, construction)

        Args:
            name: space name. (is joined with _wall_{n}).
            location: vertice of space poly anchoring the wall.
            construction: display_name of construction wall is comprised of.

    Example:

        .. code-block:: f#

            "simple_example_dfb_Floor1_Room1 Wall_1" = EXTERIOR-WALL
               CONSTRUCTION    = "EWall Construction"
               LOCATION        = SPACE-V1
               ..

    """
    name: str
    location: int
    construction: str

    @classmethod
    def from_room_seg(cls, name: str, location: int, construction: str):
        indexed_id = location + 1
        return cls(f'{name}_Wall_{indexed_id}', indexed_id, construction)

    def to_inp(self):
        return f'"{self.name}" = EXTERIOR-WALL\n' \
            f'   CONSTRUCTION    = "{self.construction}_c"\n' \
            f'   LOCATION        = SPACE-V{self.location}\n   ..'

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class Space:
    """The Space Object.
    Each Room2D has a Space obj. This obj contains windows, walls, doors
    data.

        Init method(s):
            1. from_room(room: Room2D)
        Args:
             name: room.display_name.
             activity: room program.display_name.
             walls: List[of Wall(objects)]

    Example:

        .. code-block:: f#

            "simple_example_dfb_Floor1_Room1" = SPACE
                SHAPE            = POLYGON
                POLYGON          = "simple_example_dfb_Floor1_Room1 Plg"
                C-ACTIVITY-DESC  = *Generic Office Program*
                ..
            "simple_example_dfb_Floor1_Room1 Wall_1" = EXTERIOR-WALL
                CONSTRUCTION    = "EWall Construction"
                LOCATION        = SPACE-V1
                ..
            "simple_example_dfb_Floor1_Room1 Wall_2" = EXTERIOR-WALL
                CONSTRUCTION    = "EWall Construction"
                LOCATION        = SPACE-V2
                ..

    """
    name: str
    activity: str
    walls: List[Wall]
    slab: Slab = None
    roof: RoofCeiling = None

    @classmethod
    def from_room(cls, room: Room2D):
        if not isinstance(room, Room2D):
            raise ValueError(
                f'Unsupported Type: {type(room)}.\n'
                'Expected dragonfly.room2d.Room2D'
            )

        wall_constr_name = short_name(
            room.properties.energy.construction_set.wall_set.exterior_construction.display_name, 30)
        name = room.display_name
        walls = [
            Wall.from_room_seg(name, i, wall_constr_name)
            for i, bc in enumerate(room.boundary_conditions)
            if str(bc) == 'Outdoors'
        ]
        slab = None if room.is_ground_contact != True else Slab.from_room(name, short_name(
            room.properties.energy.construction_set.floor_set.ground_construction.display_name, 30))

        roof = None if room.is_top_exposed != True else RoofCeiling.from_room(room)

        return cls(
            name=room.display_name,
            activity=room.properties.energy.program_type.display_name, walls=walls,
            slab=slab, roof=roof)

    def to_inp(self):
        space_walls = '\n'.join(wall.to_inp() for wall in self.walls)
        space_block = f'"{self.name}" = SPACE\n' \
                      f'   SHAPE           = POLYGON\n' \
                      f'   POLYGON         = "{self.name} Plg"\n' \
                      f'   C-ACTIVITY-DESC = *{self.activity}*\n   ..\n'
        blocks = [space_block, space_walls]
        if self.slab:
            blocks.append(self.slab.to_inp())
        if self.roof:
            blocks.append(self.roof.to_inp())
        return '\n'.join(blocks)

    def __repr__(self):
        return self.to_inp()


@dataclass
class Floor:
    """The *.inp 'Floor' object, contains spaces and space meta-data.

        Init method(s):
            1. from_story(story: Story).
        Args:
            name: Story display_name.
            floor_z: the height of the floor poly centroid from ground level.
            floor_height: the floor-to-floor height of the rooms within the story.
                This is a single input for eQuest, all rooms in story share this value.

    Example:

        .. code-block:: f#

            "simple_example_dfb_Floor1" = FLOOR
                Z                = 0.0
                POLYGON          = "simple_example_dfb_Floor1 Floor Plg"
                SHAPE            = POLYGON
                FLOOR-HEIGHT     = 10.0
                C-DIAGRAM-DATA   = *simple_example_dfb_Floor1 UI DiagData*
                ..
            "simple_example_dfb_Floor1_Room1" = SPACE
                SHAPE            = POLYGON
                POLYGON          = "simple_example_dfb_Floor1_Room1 Plg"
                C-ACTIVITY-DESC  = *Generic Office Program*
                ..
            "simple_example_dfb_Floor1_Room1 Wall_1" = EXTERIOR-WALL
                CONSTRUCTION    = "EWall Construction"
                LOCATION        = SPACE-V1
                ..

    """
    name: str
    floor_z: float
    floor_height: float
    spaces: List[Space]

    @classmethod
    def from_story(cls, story: Story):
        if not isinstance(story, Story):
            raise ValueError(
                f'Unsupported type: {type(story)}\n'
                'Expected dragonfly.story.Story'
            )
        spaces = [Space.from_room(room) for room in story.room_2ds]
        return cls(
            story.display_name, story.floor_height,
            story.floor_to_floor_height, spaces
        )

    def to_inp(self):
        flr_str = f'"{self.name}" = FLOOR\n' \
            f'   Z               = {self.floor_z}\n' \
            f'   POLYGON         = "{self.name} Plg"\n' \
            f'   SHAPE           = POLYGON\n' \
            f'   FLOOR-HEIGHT    = {self.floor_height}\n' \
            f'   C-DIAGRAM-DATA  = *{self.name} UI DiagData*\n   ..\n'
        flr_spcs = '\n'.join(spc.to_inp() for spc in self.spaces)
        return '\n'.join([flr_str, flr_spcs])

    def __repr__(self):
        return self.to_inp()
