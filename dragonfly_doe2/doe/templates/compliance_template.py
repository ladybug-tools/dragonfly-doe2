from dataclasses import dataclass


@dataclass()
class ComplianceData:

    permit_scope: int = 0
    proj_name: str = 'sample_project'
    bldg_type: int = 32
    cons_phase: int = 0
    nr_dhw_incl: int = 1
    code_version: int = 1
    num_floors: int = 1
    bldg_type_901: int = 32

    def to_inp(self) -> str:
        """Return compliance data as an inp string."""
        return '"Compliance Data" = COMPLIANCE\n' \
            f'   C-PERMIT-SCOPE   = {self.permit_scope}\n' \
            f'   C-PROJ-NAME      = *{self.proj_name}*\n' \
            f'   C-BUILDING-TYPE  = {self.bldg_type_901}\n' \
            f'   C-CONS-PHASE     = {self.cons_phase}\n' \
            f'   C-NR-DHW-INCL    = {self.nr_dhw_incl}\n' \
            f'   C-CODE-VERSION   = {self.code_version}\n' \
            f'   C-901-NUM-FLRS   = {self.num_floors}\n' \
            f'   C-901-BLDG-TYPE  = {self.bldg_type_901}\n' \
            '..'

    def __repr__(self) -> str:
        return self.to_inp()
