from doe.model import INPRoom, INPStory, INPModel


# TODO: refactor like hb ies from the classes in doe to do a one-shot write out from the classes
"""
Notes:
Make agnostic 'lookup classes' to use for ease of iteration
- then: step through the df_model and *.inp file and go block by block to build the file.
MO example:
   for polygon_block:
   .. code-block::python
    for story in model.stories:
        file.add(Polygon(story))
        for room in story.room_2ds:
            file.add(Polygon(room))

Polygon class does a type check which determines what template is pulled to __repr__ out
"""
