from typing import List

from dragonfly.model import Model as DFModel
from dragonfly.story import Story as DFStory
from dragonfly.room2d import Room2D as DFRoom

from ladybug.analysisperiod import AnalysisPeriod

from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.lib.constructionsets import generic_construction_set

from .polygon import Polygon
from .compliance import ComplianceData
from .sitebldg import SiteBldgData
from .title import Title
from .run_period import RunPeriod
from .construction import Construction, ConstructionCollection
from .floor_space import Floor
from .glass_types import GlassType
from .shades import Doe2ShadeCollection
from .hvac import HVACSystem

from . import blocks as fb


class Model:
    """A DOE *.inp Model File Object."""

    def __init__(self, title, run_period=None, compliance_data=None,
                 site_building_data=None, polygons=None, constructions=None, floors=None,
                 glass_types=None, context_shades=None, hvac_system_zone=None) -> None:
        self.title = title
        self.run_period = run_period
        self.compliance_data = compliance_data
        self.site_bldg_data = site_building_data
        self.polygons = polygons
        self.constructions = constructions
        self.floors = floors
        self.glass_types = glass_types
        self.context_shades = context_shades
        self.hvac_system_zone = hvac_system_zone

    @classmethod
    def from_df_model(cls, df_model: DFModel, run_period=None):
        # Make model windows rectangular to be INP friendly
        df_model.to_rectangular_windows()

        # Check model units, ensure units in feet
        df_model.convert_to_units(units='Feet')
        df_model.properties.energy.construction_sets.append(generic_construction_set)

        polygons = []
        flr_spc = []
        window_constructions = []
        context_shades = []
        hvac_system_zone = []

        window_constructions.append(
            generic_construction_set.aperture_set.window_construction)

        for con_set in df_model.properties.energy.construction_sets:
            window_constructions.append(con_set.aperture_set.window_construction)

        # purge duplicate window constructions
        window_constructions = list(set(window_constructions))

        for building in df_model.buildings:
            for story in building.all_stories():
                # enforce a recompute of floor to floor height
                if story.floor_to_floor_height == 0:
                    story.floor_to_floor_height = None

                story.solve_room_2d_adjacency(df_model.tolerance, intersect=True)

                hvac_system_zone.append(HVACSystem.from_story(story))

                flr_spc.append(Floor.from_story(story))
                polygons.append(Polygon.from_story(story))
                for room in story:
                    polygons.append(Polygon.from_room(room))

        df_envelope_constrs = []
        for con in generic_construction_set.wall_set.constructions:
            df_envelope_constrs.append(con)
        for con in generic_construction_set.floor_set.constructions:
            df_envelope_constrs.append(con)
        for con in generic_construction_set.roof_ceiling_set:
            df_envelope_constrs.append(con)
        # TODO: This messy MO takes the un-needed door constructions out of the equation
        # TODO: Make more elegant when implements "to thin, make u-val"
        for construction_set in df_model.properties.energy.construction_sets:
            for con in construction_set.wall_set.constructions:
                df_envelope_constrs.append(con)
            for con in generic_construction_set.wall_set.constructions:
                df_envelope_constrs.append(con)
            for con in construction_set.floor_set.constructions:
                df_envelope_constrs.append(con)
            for con in construction_set.roof_ceiling_set:
                df_envelope_constrs.append(con)

        constructions = ConstructionCollection.from_hb_constructions(
            df_envelope_constrs)

        glass_types = [GlassType.from_hb_window_constr(
            w_con) for w_con in window_constructions]

        shade_objs = df_model.context_shades
        context_shades.append(Doe2ShadeCollection.from_df_context_shades(shade_objs))

        return cls(
            df_model.display_name, run_period, polygons=polygons,
            constructions=constructions, floors=flr_spc, glass_types=glass_types,
            context_shades=context_shades, hvac_system_zone=hvac_system_zone)

    @classmethod
    def from_dfjson(cls, dfjson_file, run_period=None):
        model = DFModel.from_dfjson(dfjson_file)
        return cls.from_df_model(model, run_period)

    @property
    def _header(self):
        """File header.

        NOTE: The header is currently read-only
        """
        return '\n'.join([fb.top_level, fb.abort_diag])

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = Title(value)
        # update the title in complinace data
        try:
            self.compliance_data.proj_name = value
        except AttributeError:
            # this happens on initiation since compliance data is not set yet
            # we can ignore it
            pass

    @property
    def run_period(self):
        """Model run period."""
        return self._run_period

    @run_period.setter
    def run_period(self, value: AnalysisPeriod):
        self._run_period = RunPeriod.from_analysis_period(value)

    @property
    def compliance_data(self):
        """Model DOE2 Compliance Data"""
        return self._compliance_data

    @compliance_data.setter
    def compliance_data(self, value):
        if not value:
            value = ComplianceData()
        # make sure the project name is set to model title
        value.proj_name = self.title.title
        self._compliance_data = value

    @property
    def site_bldg_data(self):
        return self._site_bldg_data

    @site_bldg_data.setter
    def site_bldg_data(self, value):
        if not value:
            value = SiteBldgData()
        self._site_bldg_data = value

    @property
    def polygons(self) -> List[Polygon]:
        return self._polygons

    @polygons.setter
    def polygons(self, value):
        self._polygons = value

    @property
    def constructions(self) -> ConstructionCollection:
        return self._constructions

    @constructions.setter
    def constructions(self, value):
        self._constructions = value

    @property
    def glass_types(self):
        return self._glass_types

    @glass_types.setter
    def glass_types(self, value):
        self._glass_types = value

    @property
    def context_shades(self):
        return self._context_shades

    @context_shades.setter
    def context_shades(self, value):
        self._context_shades = value

    @property
    def hvac_system_zone(self):
        return self._hvac_system_zone

    @hvac_system_zone.setter
    def hvac_system_zone(self, value):
        self._hvac_system_zone = value

    def to_inp(self):

        data = [
            self._header,
            fb.global_params,
            fb.ttrpddh, self.title.to_inp(), self.run_period.to_inp(),
            fb.comply,
            self.compliance_data.to_inp(),
            self.site_bldg_data.to_inp(),
            self.constructions.to_inp(),
            fb.glzCode,
            '\n'.join(gt.to_inp() for gt in self.glass_types),
            fb.polygons,
            '\n'.join(pl.to_inp() for pl in self.polygons),
            fb.wallParams,
            '\n'.join(shd.to_inp() for shd in self.context_shades),
            fb.miscCost,
            fb.perfCurve,
            fb.floorNspace,
            '\n'.join(flr.to_inp() for flr in self.floors),
            fb.elecFuelMeter,
            fb.elec_meter,
            fb.fuel_meter,
            fb.master_meter,
            fb.hvac_circ_loop,
            fb.pumps,
            fb.heat_exch,
            fb.circ_loop,
            fb.chiller_objs,
            fb.boiler_objs,
            fb.dwh,
            fb.heat_reject,
            fb.tower_free,
            fb.pvmod,
            fb.elecgen,
            fb.thermal_store,
            fb.ground_loop_hx,
            fb.comp_dhw_res,
            fb.steam_cld_mtr,
            fb.steam_mtr,
            fb.chill_meter,
            fb.hvac_sys_zone,
            '\n'.join(hv_sys.to_inp() for hv_sys in self.hvac_system_zone),
            fb.misc_meter_hvac,
            fb.equip_controls,
            fb.load_manage,
            fb.big_util_rate,
            fb.ratchets,
            fb.block_charge,
            fb.small_util_rate,
            fb.output_reporting,
            fb.loads_non_hrly,
            fb.sys_non_hrly,
            fb.plant_non_hrly,
            fb.econ_non_hrly,
            fb.hourly_rep,
            fb.the_end
        ]
        return '\n\n'.join(data)

    def __repr__(self) -> str:
        return 'Doe2 Model:\n%s' % self.title.to_inp()
