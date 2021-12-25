class SiteBldgData(object):
    def __init__(self):
        super(SiteBldgData, self).__init__()

    def to_inp(self):
        """Return Site and Building Data as an inp string"""
        return '$' + ('-'*57) + '\n' \
               '$              Site and Building Data\n' \
               '$' + ('-'*57) + '\n\n' \
               '"Site Data" = SITE-PARAMETERS\n  ' \
               'ALTITUDE          = 150\n  ' \
               'C-STATE           = 21\n  ' \
               'C-WEATHER-FILE    = *TMY2\\HARTFOCT.bin* \n  ' \
               'C-COUNTRY         = 1\n  ' \
               'C-901-LOCATION    = 1092\n  ..\n' \
               '"Building Data" = BUILD-PARAMETERS\n  ' \
               'HOLIDAYS        = "Standard US Holidays"\n  ..\n\n\n' \
               'PROJECT-DATA\n  ..\n\n'

    def __repr__(self):
        return self.to_inp()
