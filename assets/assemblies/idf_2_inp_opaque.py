from honeybee_energy.construction.opaque import OpaqueConstruction as op_cons
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from honeybee_energy.constructionset import ConstructionSet
from dragonfly.model import Model as DFModel
from dragonfly_energy.properties import *
from ..templates.data_classing import IpyDataClass as ipydata


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
            pass  # TODO: Make builder, check docs to see what the input types are
            # TODO: do check for e-mat or e-mat-no-mass


class OpaqueConstr(ipydata):
    """Data Class for OpaqueConstr, currently just u-value type"""
    cons_name = None
    cons_type = 'U-VALUE'
    u_value = None

    def to_inp(self):
        """Return Opaque Construction as inp string."""
        return '"{cons_name} Construction" = CONSTRUCTION\n  '.format(
            cons_name=self.cons_name) + 'TYPE              = {cons_type}\n  '.format(
            cons_type=self.cons_type) + 'U-VALUE           = {u_value}\n  ..'.format(
            u_value=self.u_value)

    def __repr__(self) -> str:
        return self.to_inp()
