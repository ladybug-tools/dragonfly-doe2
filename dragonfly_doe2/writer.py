# coding: utf-8
"""Write an inp file from a Dragonfly model."""
from __future__ import division

from honeybee_doe2.writer import model_to_inp as hb_model_to_inp
from honeybee_doe2.simulation import SimulationPar


def model_to_inp(
    model, simulation_par=None, project_info=None,
    use_multiplier=True, exclude_plenums=False, solve_ceiling_adjacencies=True,
    merge_method='None', hvac_mapping='Story',
    exclude_interior_walls=False, exclude_interior_ceilings=False, equest_version=None,
    face_rename_format='{parent.display_name} - {gbxml_type} - {cardinal_direction}',
    subface_rename_format='{parent.parent.display_name} - {type} - {cardinal_direction}',
    name_decimal_count=None, exclude_units_in_name=False,
):
    """Generate an INP string from a Dragonfly Model.

    The resulting string will include all geometry, all fully-detailed constructions
    and materials, all fully-detailed schedules, and the room properties. It will
    also include the simulation parameters. Essentially, the string includes
    everything needed to simulate the model.

    Args:
        model: A dragonfly Model for which an INP representation will be returned.
        simulation_par: A honeybee-doe2 SimulationPar object to specify how the
            DOE-2 simulation should be run. If None, default simulation
            parameters will be generated, which will run the simulation for the
            full year. (Default: None).
        project_info: An optional ladybug ProjectInfo object that describes criteria
            about the project site. When specified, this will be used to fill in
            any information that is not described in the sim_par_json. Otherwise,
            the sim_par_json overrides whatever is specified within the
            project_info. (Default: None).
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
        merge_method: An optional text string to describe how the Room2Ds should
            be merged into individual Rooms during the translation. Specifying a
            value here can be an effective way to reduce the number of Room volumes
            in the resulting Model and, ultimately, yield a faster simulation time
            with less results to manage. Note that Room2Ds will only be merged if they
            form a contiguous volume across their solved adjacencies. Otherwise,
            there will be multiple Rooms per zone or story, each with an integer
            added at the end of their identifiers. Choose from the following options:

            * None - No merging of Room2Ds will occur
            * Zones - Room2Ds in the same zone will be merged
            * PlenumZones - Only plenums in the same zone will be merged
            * Stories - Rooms in the same story will be merged
            * PlenumStories - Only plenums in the same story will be merged

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
        face_rename_format: An optional text string for the pattern with which
            faces will be renamed. Any property on the honeybee Face class may be
            used (eg. gbxml_str) and each property should be put in curly brackets.
            Nested properties can be specified by using "." to denote nesting levels
            (eg. properties.energy.construction.display_name). Functions that
            return string outputs can also be passed here as long as these
            functions defaults specified for all arguments. If None, the names
            will match the identifiers.
        subface_rename_format: An optional text string for the pattern with which
            apertures and doors will be renamed. Any property that exists on both
            the honeybee Aperture and honeybee Door class may be used (eg. gbxml_type)
            and each property should be put in curly brackets. Nested
            properties can be specified by using "." to denote nesting levels
            (eg. properties.energy.construction.display_name). Functions that
            return string outputs can also be passed here as long as these
            functions defaults specified for all arguments. If None, the names
            will match the identifiers.
        name_decimal_count: An integer to set the number of decimal places that
            appear in face and opening names for all numerical properties.
            If None, the number of decimal places are determined by the
            model tolerance. (Default: None).
        exclude_units_in_name: Boolean for wether the units should be
            excluded from all length, area and volume attributes. (Default: False).

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
    # load simulation parameters if specified
    if simulation_par is not None:
        if project_info is not None:
            simulation_par.site.assign_from_project_info(project_info, overwrite=False)
    else:
        simulation_par = SimulationPar()
        if project_info is not None:
            simulation_par.site.assign_from_project_info(project_info, overwrite=True)

    # convert the Dragonfly Model to Honeybee
    north_angle = simulation_par.site.north_angle if project_info else 0
    hb_model = model.to_honeybee(
        'District', use_multiplier=use_multiplier, exclude_plenums=exclude_plenums,
        solve_ceiling_adjacencies=solve_ceiling_adjacencies, merge_method=merge_method,
        enforce_adj=False, enforce_solid=True,
        face_rename_format=face_rename_format, subface_rename_format=subface_rename_format,
        name_decimal_count=name_decimal_count, exclude_units_in_name=exclude_units_in_name,
        north_angle=north_angle
    )[0]

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
        hb_model, simulation_par=simulation_par,
        hvac_mapping=hvac_mapping,
        exclude_interior_walls=exclude_interior_walls,
        exclude_interior_ceilings=exclude_interior_ceilings,
        equest_version=equest_version
    )
    return inp_str
