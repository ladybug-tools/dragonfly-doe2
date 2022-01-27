from dataclasses import dataclass
from enum import unique
from typing import List

from honeybee_energy.construction.opaque import OpaqueConstruction as OpConstr

from .material import Material
from . import blocks as fb
from .utils import short_name


@dataclass
class Construction:
    name: str
    materials: List[Material]
    absorptance: float
    roughness: int

    @classmethod
    def from_hb_construction(cls, construction: OpConstr):
        """Create inp construction from HB construction."""
        roughdict = {'VeryRough': 1, 'Rough': 2, 'MediumRough': 3,
                     'MediumSmooth': 4, 'Smooth': 5, 'VerySmooth': 6}
        if not isinstance(construction, OpConstr):
            # this should raise an error but for now I leave it to print until we
            # support a handful number of types
            print(
                f'Unsupported Construction type: {type(construction)}.\n'
                'Please be patient as more features and capabilities are implemented.'
            )
            return cls(construction.display_name, [], 0, 0)

        materials = [
            Material.from_hb_material(material) for material in construction.materials
        ]
        absorptance = construction.materials[0].solar_absorptance
        roughness = roughdict[construction.materials[0].roughness]

        cons_name = short_name(construction.display_name, 30)

        return cls(cons_name, materials, absorptance, roughness)

    def to_inp(self, include_materials=True):

        # temporary solution not return values for unsupported construction types
        if not self.materials:
            return ''

        if include_materials:
            block = ['\n'.join(material.to_inp() for material in self.materials)]
        else:
            block = []

        materials = '\n      '.join(f'"{material.name}",'
                                    for material in self.materials)

        layers_name = f'"{self.name}_l"'
        construction = f'{layers_name} = LAYERS\n' \
            f'   MATERIAL             = (\n      {materials[:-1]}\n   )\n' \
            '   ..\n\n' \
            f'"{self.name}_c" = CONSTRUCTION\n' \
            '   TYPE                 = LAYERS\n' \
            f'   ABSORPTANCE          = {self.absorptance}\n' \
            f'   ROUGHNESS            = {self.roughness}\n' \
            f'   LAYERS               = {layers_name}\n' \
            '   ..\n'
        block.append(construction)

        return '\n\n'.join(block)

    def __repr__(self) -> str:
        return self.to_inp()


@dataclass
class ConstructionCollection:
    """Construction object. Contains, materials and layers for *.inp file.

        Returns:
          $  Materials / Layers / Constructions *.inp block
    """
    constructions: List[Construction]

    @classmethod
    def from_hb_constructions(cls, constructions: List[OpConstr]):
        unique_constructions = {
            construction.display_name: construction for construction in constructions
        }.values()

        constructions = [
            Construction.from_hb_construction(construction)
            for construction in unique_constructions
        ]
        return cls(constructions)

    def to_inp(self):

        block = [fb.mats_layers]

        # collect all the materials and ensure to only include the unique ones
        materials = set(
            mat.to_inp()
            for construction in self.constructions
            for mat in construction.materials
        )
        block.append('\n\n'.join(materials))

        # add constructions - layers are created as part of each construction definition
        for construction in self.constructions:
            block.append(construction.to_inp(include_materials=False))

        return '\n'.join(block)

    def __repr__(self):
        return self.to_inp()
