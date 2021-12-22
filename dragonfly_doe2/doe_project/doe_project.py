from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from dragonfly_doe2.inp_file import fileblocks as fb
from .doe_templates.polygon_template import DOEPoly


class DOEModelFile:
    """A DOE *.inp Model File Object"""

    def __init__(self, df_model, **kwargs) -> None:
        """Quick n Dirty kwargs: will be replaced with args if needed"""
        self.df_model = df_model

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def file_start(self):
        return self._make_file_start()

    @staticmethod
    def _make_file_start(_objs=None):
        # TODO:  Make this not hard coded
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

    def to_inp(self):
        # pretend itter example
        data_objs = [
            self.file_start,
        ]
        # poly block
        for story in self.df_model.stories:
            data_objs.append(DOEPoly(story))
            for room in story:
                data_objs.append(DOEPoly(room))
        # do some non-multi-level data blocks like cons mats layers
        # some point do another itter
        data = tuple(data_objs)

        return '\n\n'.join(data)

    def __repr__(self) -> str:
        # Returns the whole file to be written to output.inp
        return self.to_inp()
