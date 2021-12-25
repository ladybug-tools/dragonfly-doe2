from honeybee_energy.construction.opaque import OpaqueConstruction as OpConstr
from honeybee_energy.constructionset import constructionset as ConstrSet
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
import ladybug.datatype.UNITS as lbt_units
import ladybug.datatype.TYPESDICT as lbt_td


class Material(object):
    """Material Obj
    refer to:
        assets\DOE22Vol2-Dictionary_48r.pdf pg: 97
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

    def to_inp(self):
        if self.mat_type == 'PROPERTIES':
            return'"{display_name}" = MATERIAL\n'.format(
                display_name=self.hbmat.display_name) + \
                '   TYPE            = {mat_type}\n'.format(mat_type=self.mat_type) + \
                '   THICKNESS       = {thickness}\n'.format(
                    thickness=self.lbt_to_ip(self.hbmat.thickness, 'ft', 'm')) + \
                '   CONDUCTIVITY    = {cond}\n'.format(
                    cond=self.lbt_to_ip(self.hbmat.conductivity, 'Btu/h-ft2', 'W/m2')) + \
                '   DENSITY         = {dens}\n'.format(dens=self.hbmat.density/16.018) + \
                '   SPECIFIC-HEAT   = {spech}\n'.format(
                    spech=self.lbt_to_ip(self.hbmat.specific_heat, 'Btu/lb', 'J/kg')) + \
                '   ..'
        elif self.mat_type == 'RESISTANCE':
            return '"{display_name}" = MATERIAL\n'.format(
                display_name=self.hbmat.display_name) + \
                '   TYPE           = {mat_type}\n'.format(mat_type=self.mat_type) + \
                '   RESISTANCE     = {r_val}\n   ..'.format(
                    r_val=self.lbt_to_ip(self.hbmat.r_value, 'h-ft2-F/Btu', 'm2-K/W'))

    def __repr__(self):
        return self.to_inp()


class Construction(object):
    """Construction object. Contains, materials and layers for *.inp file.
    Intent: Pass list of constrs in dfm to this class.
    Should return enum of mats, 'layers' (stupid f'n eQuest obj imo..), Constr objs
    via __repr__
    TODO: make it happen! easy day! tomorrow.
    """

    def __init__(self, hb_constructions: list):
        self._hb_constructions = hb_constructions

    @property
    def hb_constructions(self):
        return self._hb_constructions

    # ...STATICMETHOD!! noo... nooo... ...maybe. unitl tomoz!
