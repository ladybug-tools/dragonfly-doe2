from dataclasses import dataclass


@dataclass()
class SiteBldgData:

    def to_inp(self) -> str:
        """Return Site and Building Data as an inp string"""
        return '$' + ('-'*57) + '\n' \
               '$              Site and Building Data\n' \
               '$' + ('-'*57) + '\n\n' \
               '"Site Data" = SITE-PARAMETERS\n  ' \
               'ALTITUDE          = 150\n  ' \
               'C-STATE           = 21\n  ' \
               'C-WEATHER-FILE    = *TMY2\HARTFOCT.bin*\n  ' \
               'C-COUNTRY         = 1\n  ' \
               'C-901-LOCATION    = 1092\n  ..\n' \
               '"Building Data" = BUILD-PARAMETERS\n  ' \
               'HOLIDAYS        = "Standard US Holidays"\n  ..\n\n\n' \
               'PROJECT-DATA\n  ..\n\n'

    def __repr__(self) -> str:
        return self.to_inp()
