from dragonfly.room2d import Room2D
from dragonfly.story import Story
from dataclasses import dataclass
from typing import List


@dataclass
class Wall:
    """*.inp Wall object.
    Example:
        .. code-block:: f#

            "simple_example_dfb_Floor1_Room1 Wall_1" = EXTERIOR-WALL
               CONSTRUCTION    = "EWall Construction"
               LOCATION        = SPACE-V1
               ..
    """
    name: str = ''
    location: int = 0
    construction: str = ''

    @classmethod
    def from_room_seg(cls, name: str, location: int, construction: str):
        indexed_id = location+1
        return cls(str(name+f'_Wall_{indexed_id}'), indexed_id, construction)

    def to_inp(self):
        return f'"{self.name}" = EXTERIOR-WALL\n' \
            f'   CONSTRUCTION   = "{self.construction}"\n' \
            f'   LOCATION       = SPACE-V{self.location}\n   ..'

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class Space:
    """The Space Object.
    Each Room2D has a Space obj. This obj contains windows, walls, doors
    data.
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
    name: str = ''
    activity: str = ''
    walls: List[Wall] = None

    @classmethod
    def from_room(cls, room: Room2D):
        if not isinstance(room, Room2D):
            # TODO: Make raise exception rather than print
            print(
                f'Unsupported Type: {type(room)}.\n'
                'Expected dragonfly.room2d.Room2D'
            )

        wall_constr_name = room.properties.energy.construction_set.wall_set.exterior_construction.display_name
        walls = []
        bcs = [str(bc) for bc in room.boundary_conditions]
        if 'Outdoors' in bcs:
            for i, bc in enumerate(bcs):
                if bc == 'Outdoors':
                    walls.append(Wall().from_room_seg(
                        room.display_name, i, wall_constr_name))
        else:
            walls = None

        return cls(
            name=room.display_name,
            activity=room.properties.energy.program_type.display_name, walls=walls)

    def to_inp(self):
        space_walls = '\n'.join(wall.to_inp() for wall in self.walls)
        space_block = f'"{self.name}" = SPACE\n' \
                      f'   SHAPE           = POLYGON\n' \
                      f'   POLYGON         = "{self.name} Plg"\n' \
                      f'   C-ACTIVITY-DESC = *{self.activity}*\n   ..\n'
        return space_block + space_walls

    def __repr__(self):
        return self.to_inp()


@dataclass()
class Floor:
    """The *.inp 'Floor' object, contains spaces and space meta-data.
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
    name: str = ''
    floor_z: float = 0.0
    floor_height: float = 3.0
    spaces: List[Space] = None

    @classmethod
    def from_story(cls, story: Story):
        if not isinstance(story, Story):
            # TODO: Make raise exception instead of print
            print(f'Unsupported type: {type(story)}\n'
                  'Expected dragonfy.story.Story')
        cls_ = cls()
        cls_.name = story.display_name
        cls_.floor_z = story.floor_height
        cls_.floor_height = story.floor_to_floor_height
        spcs = []
        for room in story.room_2ds:
            spcs.append(Space().from_room(room))
        cls_.spaces = spcs
        return cls_

    def to_inp(self):
        flr_str = f'"{self.name}" = FLOOR\n' \
            f'   Z                = {self.floor_z}\n' \
            f'   POLYGON          = "{self.name} Plg"\n' \
            f'   SHAPE            = POLYGON\n' \
            f'   FLOOR-HEIGHT     = {self.floor_height}\n' \
            f'   C-DIAGRAM-DATA   = *{self.name} UI DiagData*\n   ..\n'
        flr_spcs = '\n'.join(spc.to_inp() for spc in self.spaces)
        return flr_str + flr_spcs + '\n'

    def __repr__(self):
        return self.to_inp()
