from dragonfly.room2d import Room2D
from dragonfly.story import Story
from dataclasses import dataclass
from typing import List
from .utils import short_name, lower_left_properties
from dragonfly.windowparameter import RectangularWindows
from honeybee_energy.construction.window import WindowConstruction


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

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class RoofCeiling:
    # TODO: Need to add "what's on the other side" for interior adj ceilings.
    # TODO: refer to df intesect/solve adj's adj info
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

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class Window:
    """*.inp Window object.

        Args:
            name: display name of the room2d, to be added to, creating a unique displayname.
            location: the index/n of the window in the set of windows hosted by the wall
            segment.
            x: window origin pt.x coord.
            y: window origin pt.y coord.
            width: window width.
            height: window height.

    Example:
        .. code-block:: f#

            rmOne_wndw_0_wall1 = WINDOW
                X           = 0.6830601092896195
                Y           = 2.6229508196721314
                WIDTH       = 9.562841530054643
                HEIGHT      = 6.557377049180327
                GLASS-TYPE  = WT1
                ..
    """
    name: str
    location: int
    x: float
    y: float
    width: float
    height: float
    glass_type: str

    def to_inp(self):
        shortened_name = short_name(f'{self.name}_w{self.location}', 32)
        return f'"{shortened_name}" = WINDOW\n   ' \
               f'X           = {self.x}\n   ' \
               f'Y           = {self.y}\n   ' \
               f'WIDTH       = {self.width}\n   ' \
               f'HEIGHT      = {self.height}\n   '\
               f'GLASS-TYPE  = "{short_name(self.glass_type, 32)}"\n   ..\n'

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class WindowSet:
    """ An internal object comprising all of the windows hosted by a wall segment.

        Init methods(s):
            from_params(name, location, rectangular_window_params).

        Args:
            name: the display name of the room2d hosting the wall the windowset belongs to.
            location: the index of the room2D's wall segment hosting the window set. for use on
            creating unique identifier name for each window.
            windows: list of Window objects comprising the window set.


    """
    name: str
    location: int
    windows: List[Window]
    glass_type: None

    @classmethod
    def from_params(cls, name: str, location: int,
                    rectangular_window_params: list, glass_type):

        origins = [(orig.x, orig.y) for orig in rectangular_window_params.origins]
        widths = rectangular_window_params.widths
        heights = rectangular_window_params.heights
        glass_type = short_name(glass_type, 32)

        windows = []
        for i, (org, w, h) in enumerate(zip(origins, widths, heights)):
            windows.append(
                Window(
                    f'{name}_wndw_{i}', location + 1, org[0],
                    org[1],
                    w, h,
                    glass_type))
        return cls(name=name, location=location + 1, windows=windows,
                   glass_type=glass_type)

    def to_inp(self):
        return '\n'.join([wndw.to_inp() for wndw in self.windows])

    def __repr__(self) -> str:
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
    windows: RectangularWindows = None
    window_constr: WindowConstruction = None

    @classmethod
    def from_room_seg(cls, name: str, location: int, construction: str,
                      windows: None, window_constr: None):
        indexed_id = location + 1

        # shorten the name to ensure we don't create duplicate names with truncated id
        name = short_name(f'{name}_Wall_{indexed_id}', 32)

        return cls(name, indexed_id, construction, windows, window_constr)

    def to_inp(self):
        wallstr = f'"{self.name}" = EXTERIOR-WALL\n' \
                  f'   CONSTRUCTION    = "{self.construction}_c"\n' \
                  f'   LOCATION        = SPACE-V{self.location}\n   ..'

        if self.windows is not None:
            window_set = WindowSet.from_params(
                self.name, self.location, self.windows, self.window_constr)
            wall_set = [wallstr]
            wall_set.append(window_set.to_inp())
            return '\n'.join(wall_set)
        else:
            return wallstr

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

        low_l_props = lower_left_properties(room)
        bcs = low_l_props[1]
        wndw_paras = low_l_props[2]
        wndw_constr = low_l_props[3]

        walls = []
        for i, (bc, window_param) in enumerate(zip(bcs, wndw_paras)):
            if str(bc) in list(['Outdoors', 'Ground']):
                walls.append(
                    Wall.from_room_seg(
                        name, i, wall_constr_name, window_param, wndw_constr))

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

    def __repr__(self) -> str:
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
        # a hack to handle cases that floor height is not set for a floor
        # this will not work for stories that have rooms in different levels
        floor_height = story.floor_height or story.room_2ds[0].floor_height
        floor_to_floor_height = story.floor_to_floor_height
        if floor_height != story.floor_height:
            # this is file coming from Revit and we need to adjust the floor_to_floor
            # height that is calculated by Dragonfly
            floor_to_floor_height -= floor_height

        return cls(
            story.display_name, floor_height,
            floor_to_floor_height, spaces
        )
        # TODO: Add the clustering features into here

    def to_inp(self):
        flr_str = f'"{self.name}" = FLOOR\n' \
            f'   Z               = {self.floor_z}\n' \
            f'   POLYGON         = "{self.name} Plg"\n' \
            f'   SHAPE           = POLYGON\n' \
            f'   FLOOR-HEIGHT    = {self.floor_height}\n' \
            f'   C-DIAGRAM-DATA  = *{self.name} UI DiagData*\n   ..\n'
        flr_spcs = '\n'.join(spc.to_inp() for spc in self.spaces)
        return '\n'.join([flr_str, flr_spcs])

    def __repr__(self) -> str:
        return self.to_inp()
