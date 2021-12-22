from doe_project.doe_model import INPRoom, INPStory, INPModel


# TODO: refactor like hb ies from the classes in doe_project to do a one-shot write out from the classes
"""
Notes:
Make agnostic 'lookup classes' to use for ease of itteration
- then: step through the df_model and *.inp file and go block by block to build the file.
MO example:
   for polygon_block:
   .. code-block::python
    for story in model.stories:
        file.add(DOEPoly(story))
        for room in story.room_2ds:
            file.add(DOEPoly(room))

DOEPoly class does a type check which determines what template is pulled to __repr__ out
"""
