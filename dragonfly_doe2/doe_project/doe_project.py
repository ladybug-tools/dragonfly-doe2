from honeybee.model import Model as HBModel
from dragonfly.model import Model as DFModel
from dragonfly_doe2.inp_file import fileblocks as fb
from .doe_polygons import DOEPoly


class DOEModelFile:
    """A DOE *.inp Model File Object"""

    def __init__(self, df_model, **kwargs) -> None:
        """Quick n Dirty kwargs: will be replaced with args if needed"""
        self.df_model = df_model

        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_inp(self):
        # pretend itter example
        data_objs = []
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
