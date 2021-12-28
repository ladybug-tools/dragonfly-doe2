"""Compliance Data."""


class ComplianceData(object):

    permit_scope = 0
    proj_name = 'sample_project'
    bldg_type = 32
    cons_phase = 0
    nr_dhw_incl = 1
    code_version = 1
    num_floors = 1
    bldg_type_901 = 32

    def __init__(self):
        super(ComplianceData, self).__init__()

    def to_inp(self):
        """Return compliance data as an inp string."""
        return '"Compliance Data" = COMPLIANCE\n' \
            '   C-PERMIT-SCOPE   = {permit_scope}\n'.format(permit_scope=self.permit_scope) + \
            '   C-PROJ-NAME      = *{proj_name}*\n'.format(proj_name=self.proj_name) + \
            '   C-BUILDING-TYPE  = {bldg_type}\n'.format(bldg_type=self.bldg_type) + \
            '   C-CONS-PHASE     = {cons_phase}\n'.format(cons_phase=self.cons_phase) + \
            '   C-NR-DHW-INCL    = {nr_dhw_incl}\n'.format(nr_dhw_incl=self.nr_dhw_incl) + \
            '   C-CODE-VERSION   = {code_version}\n'.format(code_version=self.code_version) + \
            '   C-901-NUM-FLRS   = {num_floors}\n'.format(num_floors=self.num_floors) + \
            '   C-901-BLDG-TYPE  = {bldg_type_901}\n'.format(bldg_type_901=self.bldg_type_901) + \
            '   ..'

    def __repr__(self):
        return self.to_inp()
