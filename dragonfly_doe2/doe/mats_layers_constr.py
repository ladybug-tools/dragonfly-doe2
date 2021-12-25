from dataclasses import dataclass
from enum import Enum
from typing import Union

from honeybee_energy.construction.opaque import OpaqueConstruction as OpConstr
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from ladybug.datatype import UNITS as lbt_units, TYPESDICT as lbt_td

from . import blocks as fb


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
    return value


@dataclass
class NoMassMaterial:

    name: str
    resistance: float

    @classmethod
    def from_hb_material(cls, material: EnergyMaterialNoMass):
        resistance = _unit_convertor([material.r_value], 'h-ft2-F/Btu', 'm2-K/W')
        return cls(material.display_name, resistance)

    def to_inp(self):
        return f'"{self.name}" = MATERIAL\n' \
            f'   TYPE           = {MaterialType.no_mass}\n' \
            f'   RESISTANCE     = {self.resistance}\n' \
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
        name = material.display_name
        thickness = _unit_convertor([material.thickness], 'ft', 'm')
        conductivity = _unit_convertor([material.conductivity], 'Btu/h-ft2', 'W/m2')
        density = _unit_convertor(material.density/16.018)
        specific_heat = _unit_convertor([material.specific_heat], 'Btu/lb', 'J/kg')
        return cls(
                name, thickness, conductivity, density, specific_heat
        )

    def to_inp(self):
        return f'"{self.name}" = MATERIAL\n' \
            f'   TYPE            = {MaterialType.mass}\n' \
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


@dataclass
class MatsLayersConstructions(object):
    """Construction object. Contains, materials and layers for *.inp file.
    Intent: Pass list of constrs in dfm to this class.
    Should return enum of mats, 'layers' (stupid f'n eQuest obj imo..), Constr objs
    via __repr__.

        Returns:
          $  Materials / Layers / Constructions *.inp block
    """
    inp_constructions: list = None
    inp_layers: list = None
    inp_materials: list = None

    @classmethod
    def from_hb_constructions(cls, hb_constructions: list):
        """Create input data for eQuest $ Materials / Layers / Constructions *.inp block"""
        roughdict = {'VeryRough': 1, 'Rough': 2, 'MediumRough': 3,
                     'MediumSmooth': 4, 'Smooth': 5, 'VerySmooth': 6}
        cls_ = cls()
        inp_cons = []
        inp_layrs = []
        inp_mats = []
        for i, constr in enumerate(hb_constructions):
            if type(constr) == OpConstr:
                mats = [mat for mat in constr.materials]

                for mat in mats:
                    inp_mats.append(Material(mat))

                matstr = ''.join(f'"{m.display_name}", ' for m in mats)
                inp_layrs.append(
                    f'"{constr.display_name}_{i} Layers" = LAYERS\n'
                    f'   MATERIAL                 = ( {matstr} )\n   ..\n')

                inp_cons.append(
                    f'"{constr.display_name}_{i}" = CONSTRUCTION\n'
                    f'   TYPE                 = LAYERS\n'
                    f'   ABSORPTANCE          = {constr.materials[0].solar_absorptance}\n'
                    f'   ROUGHNESS            = {roughdict[constr.materials[0].roughness]}\n'
                    f'   LAYERS               = "{constr.display_name}_{i} Layers"\n   ..\n')

        cls_.inp_constructions = inp_cons
        cls_.inp_layers = inp_layrs
        cls_.inp_materials = inp_mats
        return(cls_)

    def to_inp(self):
        # ? if these could be list comps that would be chill,
        # TODO: Look at replacing with lambda func

        block = fb.matslayers
        for mat in self.inp_materials:
            block += mat.to_inp()
        for lay in self.inp_layers:
            block += lay
        for cons in self.inp_constructions:
            block += cons
        return(block)

    def __repr__(self):
        return self.to_inp()
