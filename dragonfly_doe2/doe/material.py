from dataclasses import dataclass
from enum import Enum
from typing import Union

from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from ladybug.datatype import UNITS as lbt_units, TYPESDICT as lbt_td
from .utils import short_name


class MaterialType(Enum):
    """Doe2 material types."""
    mass = 'PROPERTIES'
    no_mass = 'RESISTANCE'


def _unit_convertor(value, to_, from_):
    """Helper function to convert values from one unit to another."""
    for key in lbt_units:
        if from_ in lbt_units[key]:
            base_type = lbt_td[key]()
            break
    else:
        raise ValueError(f'Invalid type: {from_}')

    value = base_type.to_unit(value, to_, from_)
    return round(value[0], 3)


@dataclass
class NoMassMaterial:
    name: str
    resistance: float

    @classmethod
    def from_hb_material(cls, material: EnergyMaterialNoMass):
        resistance = _unit_convertor([material.r_value], 'h-ft2-F/Btu', 'm2-K/W')
        return cls(short_name(material.display_name, 32), resistance)

    def to_inp(self):
        return f'"{self.name}" = MATERIAL\n' \
            f'   TYPE            = {MaterialType.no_mass.value}\n' \
            f'   RESISTANCE      = {self.resistance}\n' \
            '   ..'


@dataclass
class MassMaterial:

    name: str
    thickness: float
    conductivity: str
    density: float
    specific_heat: float

    @classmethod
    def from_hb_material(cls, material: EnergyMaterial):
        name = short_name(material.display_name, 32)
        thickness = _unit_convertor([material.thickness], 'ft', 'm')
        conductivity = _unit_convertor([material.conductivity], 'Btu/h-ft2', 'W/m2')
        density = round(material.density / 16.018, 3)
        specific_heat = _unit_convertor([material.specific_heat], 'Btu/lb', 'J/kg')
        return cls(
            name, thickness, conductivity, density, specific_heat
        )

    def to_inp(self):
        return f'"{self.name}" = MATERIAL\n' \
            f'   TYPE            = {MaterialType.mass.value}\n' \
            f'   THICKNESS       = {self.thickness}\n' \
            f'   CONDUCTIVITY    = {self.conductivity}\n' \
            f'   DENSITY         = {self.density}\n' \
            f'   SPECIFIC-HEAT   = {self.specific_heat}\n' \
            '   ..'


@dataclass
class Material:
    """Do2 Material object.

    refer to:
        assets/DOE22Vol2-Dictionary_48r.pdf pg: 97
    """
    material: Union[NoMassMaterial, MassMaterial]

    @classmethod
    def from_hb_material(cls, material: Union[EnergyMaterial, EnergyMaterialNoMass]):
        if isinstance(material, EnergyMaterial):
            return MassMaterial.from_hb_material(material)
        elif isinstance(material, EnergyMaterialNoMass):
            return NoMassMaterial.from_hb_material(material)
        else:
            raise ValueError(f'{type(material)} type is not supported for materials.')

    def to_inp(self) -> str:
        return self.material.to_inp()

    def __repr__(self):
        return self.to_inp()
