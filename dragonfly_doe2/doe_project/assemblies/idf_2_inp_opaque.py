from dataclasses import dataclass
from honeybee_energy.construction.opaque import OpaqueConstruction as op_cons
from honebee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from honeybee_energy.constructionset import ConstructionSet
from dragonfly.model import Model as DFModel
from dragonfly_energy.properties import *


class OpaqueAssyConvert:
    def __init__(self):
        self.materials = []
        self.cons_layers = []
        self.constructions = []

    @classmethod
    def from_df_model(cls, df_model):
        cls_ = cls()
        for const in df_model.properties.energy.constructions:
            cons_obj = OpaqueConstr()
            cons_obj.cons_name = const.display_name
            cons_obj.u_value = const.u_value
            cls_.constructions.append(cons_obj)

        for mat in df_model.properties.energy.materials:
            pass


@dataclass()
class OpaqueConstr:
    cons_name: str = None
    cons_type: str = 'U-VALUE'
    u_value: float = None

    def to_inp(self) -> str:
        """Return Opaque Construction as inp string."""
        return f'"{self.cons_name} Construction" = CONSTRUCTION\n  ' \
               f'TYPE              = {self.cons_type}\n  ' \
               f'U-VALUE           = {self.u_value}\n  ..'

    def __repr__(self) -> str:
        return self.to_inp()
