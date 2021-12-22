from dataclasses import dataclass
from honeybee_energy.construction.opaque import OpaqueConstruction as op_cons
from honebee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from honeybee_energy.constructionset import ConstructionSet
from dragonfly.model import Model as DFModel
from dragonfly_energy.properties import *


class OpaqueConstrConvert:
    def __init__(self):
        self.constrs = []

    @classmethod
    def from_df_model(cls, df_model):
        cls_ = cls()
        for const in df_model.properties.energy.constructions:
            pass
