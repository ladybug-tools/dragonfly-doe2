from dataclasses import dataclass
from enum import Enum
from typing import Union

from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing, \
    EnergyWindowMaterialSimpleGlazSys

from honeybee_energy.construction.window import WindowConstruction

from .utils import short_name, unit_convertor


@dataclass
class GlassType:
    """ Doe2 glass type, (window construction) """
    name: str
    shading_coef: float
    glass_cond: float

    @classmethod
    def from_hb_window_constr(cls, window_constr: WindowConstruction):
        simple_window_con = window_constr.to_simple_construction()
        simple_window_mat = simple_window_con.materials[0]

        shading_coef = simple_window_mat.shgc / 0.87

        glass_cond = unit_convertor(
            [simple_window_mat.u_factor], 'Btu/h-ft2-F', 'W/m2-K')

        name = simple_window_con.identifier
        name = short_name(name, 32)

        return cls(name=name, shading_coef=shading_coef, glass_cond=glass_cond)

    def to_inp(self) -> str:
        return f'"{self.name}" = GLASS-TYPE\n' \
               f'   TYPE               = SHADING-COEF\n' \
               f'   SHADING-COEF       = {self.shading_coef}\n' \
               f'   GLASS-CONDUCT      = {self.glass_cond}\n' \
               f'   ..'

    def __repr__(self):
        return self.to_inp()
