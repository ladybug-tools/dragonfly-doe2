from honeybee_energy.construction.opaque import OpaqueConstruction as OpConstr
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
import ladybug.datatype
from ladybug.datatype import UNITS as lbt_units
from ladybug.datatype import TYPESDICT as lbt_td
from dataclasses import dataclass
from . import blocks as fb


class Material(object):
    """Material Obj
    refer to:
        assets\\DOE22Vol2-Dictionary_48r.pdf pg: 97
    """

    def __init__(self, _hbmat):
        self._hbmat = _hbmat

    @property
    def hbmat(self):
        return self._hbmat

    @property
    def mat_type(self):
        return self.check_mat(self.hbmat)

    @staticmethod
    def check_mat(_hbmat_mat):
        if type(_hbmat_mat) == EnergyMaterial:
            return 'PROPERTIES'
        elif type(_hbmat_mat) == EnergyMaterialNoMass:
            return 'RESISTANCE'

    def lbt_to_ip(self, _val, _to, _from):
        """Have a little LBT 4 :: Extra: with your class too!
        Thought: adhearing to utilizing LBT SDK as much as possible,
        significantly reduces probability of human(trevor) error
        """
        base_type = None
        for key in lbt_units:
            if _from in lbt_units[key]:
                base_type = lbt_td[key]()
                break
        value = base_type.to_unit(_val, _to, _from)
        return(value)

    def to_inp(self) -> str:
        # TODO: for sake of OCD: revert to 3.x f'strings'
        if self.mat_type == 'PROPERTIES':

            return'\n"{display_name}" = MATERIAL\n'.format(
                display_name=self.hbmat.display_name) + \
                '   TYPE            = {mat_type}\n'.format(mat_type=self.mat_type) + \
                '   THICKNESS       = {thickness}\n'.format(
                    thickness=self.lbt_to_ip([self.hbmat.thickness], 'ft', 'm')) + \
                '   CONDUCTIVITY    = {cond}\n'.format(
                    cond=self.lbt_to_ip([self.hbmat.conductivity], 'Btu/h-ft2', 'W/m2')) + \
                '   DENSITY         = {dens}\n'.format(dens=self.hbmat.density/16.018) + \
                '   SPECIFIC-HEAT   = {spech}\n'.format(
                    spech=self.lbt_to_ip([self.hbmat.specific_heat], 'Btu/lb', 'J/kg')) + \
                '   ..'
        elif self.mat_type == 'RESISTANCE':
            return '"{display_name}" = MATERIAL\n'.format(
                display_name=self.hbmat.display_name) + \
                '   TYPE           = {mat_type}\n'.format(mat_type=self.mat_type) + \
                '   RESISTANCE     = {r_val}\n   ..\n'.format(
                    r_val=self.lbt_to_ip([self.hbmat.r_value], 'h-ft2-F/Btu', 'm2-K/W'))

    def __repr__(self):
        return self.to_inp()


@dataclass()
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
