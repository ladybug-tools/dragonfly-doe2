# coding: utf-8
"""Write an inp file from a Dragonfly model."""
from __future__ import division

from honeybee_doe2.writer import model_to_inp as hb_model_to_inp


def model_to_inp(
    model, use_multiplier=True, exclude_plenums=False, solve_ceiling_adjacencies=True,
    simulation_par=None, hvac_mapping='Story',
    exclude_interior_walls=False, exclude_interior_ceilings=False, equest_version=None
):
    """Generate an INP string from a Dragonfly Model.

    The resulting string will include all geometry, all fully-detailed constructions
    and materials, all fully-detailed schedules, and the room properties. It will
    also include the simulation parameters. Essentially, the string includes
    everything needed to simulate the model.

    Args:
        model: A dragonfly Model for which an INP representation will be returned.
        use_multiplier: Boolean to note if the multipliers on each Building
            story will be passed along to the generated Honeybee Room objects
            or if full geometry objects should be written for each story in the
            building. (Default: True).
        exclude_plenums: Boolean to indicate whether ceiling/floor plenum depths
            assigned to Room2Ds should generate distinct 3D Rooms in the
            translation. (Default: False).
        solve_ceiling_adjacencies: Boolean to indicate whether adjacencies should
            be solved between interior stories when Room2Ds perfectly match one
            another in their floor plate. This ensures that Surface boundary
            conditions are used instead of Adiabatic ones. (Default: True).
        simulation_par: A honeybee-doe2 SimulationPar object to specify how the
            DOE-2 simulation should be run. If None, default simulation
            parameters will be generated, which will run the simulation for the
            full year. (Default: None).
        hvac_mapping: Text to indicate how HVAC systems should be assigned to the
            exported model. Story will assign one HVAC system for each distinct
            level polygon, Model will use only one HVAC system for the whole model
            and AssignedHVAC will follow how the HVAC systems have been assigned
            to the Rooms.properties.energy.hvac. Choose from the options
            below. (Default: Story).

            * Room
            * Story
            * Model
            * AssignedHVAC

        exclude_interior_walls: Boolean to note whether interior wall Faces
            should be excluded from the resulting string. (Default: False).
        exclude_interior_ceilings: Boolean to note whether interior ceiling
            Faces should be excluded from the resulting string. (Default: False).
        equest_version: An optional text string to denote the version of eQuest
            for which the INP definition will be generated. If unspecified
            or unrecognized, the latest version of eQuest will be used.

    Usage:

    .. code-block:: python

        import os
        from ladybug.futil import write_to_file
        from ladybug_geometry.geometry3d import Point3D, Face3D
        from dragonfly.model import Model
        from dragonfly.building import Building
        from dragonfly.story import Story
        from dragonfly.room2d import Room2D
        from dragonfly.roof import RoofSpecification
        from dragonfly.windowparameter import SimpleWindowRatio
        from honeybee.config import folders

        # Crate an input Model
        pts1 = (Point3D(0, 0, 0), Point3D(10, 0, 0),
                Point3D(10, 10, 0), Point3D(0, 10, 0))
        pts2 = (Point3D(10, 0, 0), Point3D(20, 0, 0),
                Point3D(20, 10, 0), Point3D(10, 10, 0))
        pts3 = (Point3D(0, 0, 3.25), Point3D(20, 0, 3.25),
                Point3D(20, 5, 5), Point3D(0, 5, 5))
        pts4 = (Point3D(0, 5, 5), Point3D(20, 5, 5),
                Point3D(20, 10, 3.25), Point3D(0, 10, 3.25))
        room2d_full = Room2D(
            'R1-full', floor_geometry=Face3D(pts1), floor_to_ceiling_height=4,
            is_ground_contact=True, is_top_exposed=True)
        room2d_plenum = Room2D(
            'R2-plenum', floor_geometry=Face3D(pts2), floor_to_ceiling_height=4,
            is_ground_contact=True, is_top_exposed=True)
        room2d_plenum.ceiling_plenum_depth = 1.0
        roof = RoofSpecification([Face3D(pts3), Face3D(pts4)])
        story = Story('S1', [room2d_full, room2d_plenum])
        story.roof = roof
        story.solve_room_2d_adjacency(0.01)
        story.set_outdoor_window_parameters(SimpleWindowRatio(0.4))
        building = Building('Office_Building_1234', [story])
        model = Model('NewDevelopment1', [building])

        # create the INP string for the model
        inp_str = model.to.inp(model)

        # write the final string into an INP
        inp = os.path.join(folders.default_simulation_folder, 'test_file', 'in.inp')
        write_to_file(inp, inp_str, True)
    """
    # convert the Dragonfly Model to Honeybee
    hb_model = model.to_honeybee(
        'District', use_multiplier=use_multiplier, exclude_plenums=exclude_plenums,
        solve_ceiling_adjacencies=solve_ceiling_adjacencies,
        enforce_adj=False, enforce_solid=True)[0]

    # assign the space polygon geometry to the Honeybee Rooms from Dragonfly
    df_flr_geos = {}  # dictionary to hold the DOE-2 space polygon geometry
    for df_room in model.room_2ds:
        df_flr_geos[df_room.identifier] = df_room.floor_geometry
    for hb_room in hb_model.rooms:
        try:
            hb_room.properties.doe2.space_polygon_geometry = \
                df_flr_geos[hb_room.identifier]
        except KeyError:  # possibly a 3D Room that has no Room2D geometry
            pass

    # patch missing adjacencies to adiabatic in case the models is a sub-selection
    hb_model.properties.energy.missing_adjacencies_to_adiabatic()

    # translate the Honeybee Model to INP
    inp_str = hb_model_to_inp(
        hb_model, simulation_par=simulation_par, hvac_mapping=hvac_mapping,
        exclude_interior_walls=exclude_interior_walls,
        exclude_interior_ceilings=exclude_interior_ceilings,
        equest_version=equest_version)
    return inp_str
