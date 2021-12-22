from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from dragonfly_doe2.inp_file import fileblocks as fb
from .doe_templates.polygon_template import DOEPoly
from .doe_templates.compliance_template import ComplianceData


class DOEModelFile:
    """A DOE *.inp Model File Object"""

    def __init__(self, df_model, **kwargs) -> None:
        """Quick n Dirty kwargs: will be replaced with args if needed"""
        self.df_model = df_model
        self.compliance_data = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def file_start(self):
        return self._make_file_start()

    @staticmethod
    def _make_file_start(_objs=None):
        # TODO:  Make this not hard coded
        # TODO:  Add this into doe_templates and make a class that takes an LB analysis period
        block = fb.topLevel+fb.abortDiag+fb.globalParam+fb.ttrpddh + \
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
        return(block)

    @property
    def compliance_data(self):
        """Get or set the model DOE2 Compliance Data"""
        return self._compliance_data

    @compliance_data.setter
    def compliance_data(self, value):
        if not value:
            value = ComplianceData()
        self._compliance_data = value

    def to_inp(self):

        polyblock = [fb.polygons]

        for story in self.df_model.stories:
            polyblock.append(DOEPoly(story))
            for room in story:
                polyblock.append(DOEPoly(room))

        polyblock = '\n\n'.join(tuple(polyblock))

        data_objs = [
            self.file_start, self.compliance_data,


        ]
        data = tuple(data_objs)

        return '\n\n'.join(data)

    def __repr__(self) -> str:
        # Returns the whole file to be written to output.inp
        return self.to_inp()
