from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from dragonfly_doe2.inp_file import fileblocks as fb
from .doe_templates.polygon_template import DOEPoly
from .doe_templates.compliance_template import ComplianceData
from .doe_templates.sitebldg_template import SiteBldgData


class DOEModelFile:
    """A DOE *.inp Model File Object"""

    def __init__(self) -> None:
        """Quick n Dirty kwargs: will be replaced with args if needed"""
        self.df_model = None
        self.file_start = None
        self.compliance_data = None

    @classmethod
    def from_df_model(cls, df_model: DFModel):
        cls_ = cls()
        cls_.df_model = df_model
        cls_.compliance_data.proj_name = df_model.identifier
        return cls_

    @property
    def file_start(self):
        return self._file_start

    @file_start.setter
    def _make_file_start(self, value):
        if not value:
            # TODO:  Make this not hard coded
            # TODO:  Add this into doe_templates and make a class that takes an LB analysis period
            value = fb.topLevel+fb.abortDiag+fb.globalParam+fb.ttrpddh + \
                'TITLE\n  LINE-1          = *simple_example*\n  ..\n\n' + \
                '"Entire Year" = RUN-PERIOD-PD\n  ' + \
                'BEGIN-MONTH     = 1\n  ' + \
                'BEGIN-DAY      = 1\n  ' + \
                'BEGIN-YEAR     = 2021\n  ' + \
                'END-MONTH      = 12\n  ' + \
                'END-DAY        = 31\n  ' + \
                'END-YEAR       = 2021\n  ..\n\n' + \
                '"Standard US Holidays" = HOLIDAYS\n  ' + \
                'LIBRARY-ENTRY "US"\n  ..\n\n'
        self._file_start = value

    @property
    def compliance_data(self):
        """Get or set the model DOE2 Compliance Data"""
        return self._compliance_data

    @compliance_data.setter
    def compliance_data(self, value):
        if not value:
            value = ComplianceData()
        self._compliance_data = value

    @property
    def site_bldg_data(self):
        return self._site_bldg_data

    @site_bldg_data.setter
    def site_bldg_data(self, value):
        if not value:
            value = SiteBldgData()
        self._site_bldg_data = value

    def to_inp(self):

        polyblock = [fb.polygons]

        for story in self.df_model.stories:
            polyblock.append(DOEPoly(story))
            for room in story:
                polyblock.append(DOEPoly(room))

        polyblock = '\n\n'.join(tuple(polyblock))

        data_objs = [
            self.file_start, self.compliance_data,
            self.site_bldg_data,

        ]
        data = tuple(data_objs)

        return '\n\n'.join(data)

    def __repr__(self) -> str:
        # Returns the whole file to be written to output.inp
        return self.to_inp()
