# coding=utf-8
from dragonfly.properties import ModelProperties, BuildingProperties, StoryProperties, \
    Room2DProperties, ContextShadeProperties
import dragonfly.writer.model as model_writer

from .properties.model import ModelDOE2Properties
from .properties.building import BuildingDOE2Properties
from .properties.story import StoryDOE2Properties
from .properties.room2d import Room2DDOE2Properties
from .properties.context import ContextShadeDOE2Properties
from .writer import model_to_doe2


# set a hidden doe2 attribute on each core geometry Property class to None
# define methods to produce doe2 property instances on each Property instance
ModelProperties._doe2 = None
BuildingProperties._doe2 = None
StoryProperties._doe2 = None
Room2DProperties._doe2 = None
ContextShadeProperties._doe2 = None


def model_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = ModelDOE2Properties(self.host)
    return self._doe2


def building_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = BuildingDOE2Properties(self.host)
    return self._doe2


def story_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = StoryDOE2Properties(self.host)
    return self._doe2


def room2d_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = Room2DDOE2Properties(self.host)
    return self._doe2


def context_doe2_properties(self):
    if self._doe2 is None:
        self._doe2 = ContextShadeDOE2Properties(self.host)
    return self._doe2


# add doe2 property methods to the Properties classes
ModelProperties.doe2 = property(model_doe2_properties)
BuildingProperties.doe2 = property(building_doe2_properties)
StoryProperties.doe2 = property(story_doe2_properties)
Room2DProperties.doe2 = property(room2d_doe2_properties)
ContextShadeProperties.doe2 = property(context_doe2_properties)

# add model writer to doe2
model_writer.doe2 = model_to_doe2
