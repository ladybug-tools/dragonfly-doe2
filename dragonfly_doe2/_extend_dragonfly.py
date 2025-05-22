# coding=utf-8
from dragonfly.properties import ModelProperties, Room2DProperties
import dragonfly.writer.model as model_writer

from .properties.model import ModelDoe2Properties
from .properties.room2d import Room2DDoe2Properties
from .writer import model_to_inp


# set a hidden doe2 attribute on each core geometry Property class to None
# define methods to produce doe2 property instances on each Property instance
ModelProperties._doe2 = None
Room2DProperties._doe2 = None


def model_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = ModelDoe2Properties(self.host)
    return self._doe2


def room2d_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = Room2DDoe2Properties(self.host)
    return self._doe2


# add doe2 property methods to the Properties classes
ModelProperties.doe2 = property(model_doe2_properties)
Room2DProperties.doe2 = property(room2d_doe2_properties)

# add writers to the honeybee-core modules
model_writer.inp = model_to_inp
