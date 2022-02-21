from dataclasses import dataclass
from typing import List
from dragonfly.model import Model
from dragonfly.context import ContextShade
from dragonfly import shadingparameter as shade_params
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Vector3D
from ladybug_geometry.geometry3d.line import LineSegment3D
from .utils import short_name
from . import blocks as fb
from math import degrees, isclose
import math


@dataclass
class Doe2Shade:
    # TODO: will need to change things up to support rm2d.shade_params
    """ DOE2 shade object. Can be either:
    -  'FIXED-SHADE': azimuth is independent from the building, i.e context shade such as
        buildings and terrain. Objects that are independent from the orientation of the 
        building during ASHRAE 90.1 baseline orientation averages. 
    -  'BUILDING-SHADE': azimuth is connected to the buildign azimuth,
          will rotate withh the building on change of azimuth, i.e fin shades, awnings, and
          other types of "on building" shading devices.

    """
    name: str
    shade_type: str
    height: float
    width: float
    x_ref: float
    y_ref: float
    z_ref: float
    azimuth: float
    tilt: float
    transmittance: float = 0.0

    @classmethod
    def from_face3d(cls, face: Face3D, indx_identifier, shade_type=None):
        """Create DOE2 shade object from Face3D object"""
        face_len_one = LineSegment3D.from_end_points(
            face.vertices[0], face.vertices[2]).length
        face_len_two = LineSegment3D.from_end_points(
            face.vertices[1], face.vertices[3]).length

        face = face if isclose(face_len_one, face_len_two) else \
            Face3D.from_regular_polygon(face.boundary_polygon2d)

        face = face if face.normal.z <= 0 else face.flip()
        shade_type = "FIXED-SHADE" if shade_type == None else shade_type
        orig_point = face.lower_left_corner
        x_ref, y_ref, z_ref = orig_point[0], orig_point[1], orig_point[2]

        height = abs(round(LineSegment3D.from_end_points(
            face.upper_right_corner, face.lower_right_corner).length, 4))
        # ? I don't like the lack of uniformity between the height and width methods; but it DOES work..
        width = face.plane.xyz_to_xy(face.max) - face.plane.xyz_to_xy(face.min)
        width = abs(round(width[0], 4))

        tilt = round(degrees(face.normal.angle(Vector3D(0, 0, 1))), 0)
        y_axis = Vector3D(0, 1, 0)
        projected_normal = Vector3D(face.normal[0], face.normal[1], 0)
        try:
            azimuth = math.degrees(projected_normal.angle(y_axis))
            cross = face.normal.cross(y_axis)
            if cross.z < 0:
                azimuth = 360 - azimuth
        except ZeroDivisionError:
            # horizontal
            azimuth = 180 if face.normal.z > 0 else -180

        return cls(
            name=indx_identifier, shade_type=shade_type, height=height, width=width,
            x_ref=x_ref, y_ref=y_ref, z_ref=z_ref, azimuth=azimuth, tilt=tilt)

    def to_inp(self):
        """Returns *.inp shade object string"""
        return f'{self.name}   = {self.shade_type}\n   ' \
            f'HEIGHT           = {self.height}\n   ' \
            f'WIDTH            = {self.width}\n   ' \
            f'TRANSMITTANCE    = {self.transmittance}\n   ' \
            f'X-REF            = {self.x_ref}\n   ' \
            f'Y-REF            = {self.y_ref}\n   ' \
            f'Z-REF            = {self.z_ref}\n   ' \
            f'AZIMUTH          = {self.azimuth}\n   ' \
            f'TILT             = {self.tilt}\n   ..'

    def __repr__(self):
        return self.to_inp()


@dataclass
class Doe2ShadeCollection:

    doe_shades: List[Doe2Shade]

    @classmethod
    def from_df_context_shades(cls, df_shades: [ContextShade]):
        """Generate doe2 fixed shades from dragonfly context shades"""
        shade_faces = []

        for shade_i, shade in enumerate(df_shades):
            for i, geom in enumerate(shade.geometry):
                shade_geom_name = f"shade_{shade_i}_geom{i}"
                shade_faces.append((geom, shade_geom_name))
        doe_shades = [Doe2Shade.from_face3d(obj[0], obj[1]) for obj in shade_faces]

        return cls(doe_shades=doe_shades)

    def to_inp(self):

        block = [fb.fix_bldg_shade]
        shades = [shade.to_inp() for shade in self.doe_shades]

        block.append('\n\n'.join(shades))

        return '\n'.join(block)

    def __repr__(self):
        return self.to_inp()
