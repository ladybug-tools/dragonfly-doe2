from dragonfly.room2d import Room2D
from dragonfly.story import Story
from dataclasses import dataclass
from typing import List


@dataclass
class Floor:
    """The *.inp:
    $ **      Floors / Spaces / Walls / Windows / Doors      **
    Object.
    """
    name: str
    floor_z: float
    floor_heigh: float
    spaces: List[Space]

    @classmethod
    def from_story(cls, story: Story):
        cls_ = cls()
        cls_.name = story.display_name
        cls_.floor_z = story.floor_heigh
        cls_.floor_heigh = story.floor_to_floor_height
        spcs = []
        for room in story.room_2ds:
            spcs.append(Space().from_room(room))
        cls_.spaces = spcs
        return cls_

    def to_inp(self):
        pass


@dataclass
class Space:
    """The Space Object.
    Each Room2D has a Space obj. This obj contains windows, walls, doors
    data.
    """
    name: str
    activity: str
    walls: List[Wall]

    @classmethod
    def from_room(cls, room: Room2D):
        if not isinstance(room, Room2D):
            # should raise error, for now; print
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
            walls = [None]

        return cls(room.display_name, room.properties.energy.program_type.display_name, walls)

    def to_inp(self):
        space_walls = '\n'.join(wall.to_inp()
                                for wall in self.walls) if None not in self.walls else None
        space_block = f'"{self.name}" = SPACE\n' \
                      f'   SHAPE           = POLYGON\n' \
                      f'   POLYGON         = "{self.name} Plg"\n' \
                      f'   C-ACTIVITY-DESC = *{self.activity}*\n   ..\n'
        return space_block.join(space_walls)

    def __repr__(self):
        return self.to_inp()


@dataclass
class Wall:
    """*.inp Wall object.
    Example:
        .. code-block::f#
            "simple_example_dfb_Floor1_Room1 Wall_1" = EXTERIOR-WALL
               CONSTRUCTION    = "EWall Construction"
               LOCATION        = SPACE-V1
               ..
    """
    name: str
    location_index: int
    wall_con_name: str

    @classmethod
    def from_room_seg(cls, _name: str, _bc_id: int, _wall_con_name: str):
        indexed_id = _bc_id+1
        return cls(str(_name+f'_Wall_{indexed_id}'), indexed_id, _wall_con_name)

    def to_inp(self):
        return f'"{self.name}" = EXTERIOR-WALL\n' \
            f'   CONSTRUCTION   = {self.exposed_wall_constr_name}\n' \
            f'   LOCATION       = SPACE-V{self.location_index}\n   ..'

    def __repr__(self) -> str:
        return self.to_inp()
