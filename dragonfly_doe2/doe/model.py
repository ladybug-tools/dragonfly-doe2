from typing import List

from dragonfly.model import Model as DFModel

from ladybug.analysisperiod import AnalysisPeriod

from .polygon import Polygon
from .compliance import ComplianceData
from .sitebldg import SiteBldgData
from .title import Title
from .run_period import RunPeriod
from .construction import Construction, ConstructionCollection
from .floor_space import Floor

from . import blocks as fb


class Model:
    """A DOE *.inp Model File Object."""

    def __init__(
            self, title, run_period=None, compliance_data=None, site_building_data=None,
            polygons=None, constructions=None, floors=None
    ) -> None:
        self.title = title
        self.run_period = run_period
        self.compliance_data = compliance_data
        self.site_bldg_data = site_building_data
        self.polygons = polygons
        self.constructions = constructions
        self.floors = floors

    @classmethod
    def from_df_model(cls, df_model: DFModel, run_period=None):
        polygons = []
        flr_spc = [Floor.from_story(story) for story in df_model.stories]

        for story in df_model.stories:
            polygons.append(Polygon.from_story(story))
            for room in story:
                polygons.append(Polygon.from_room(room))

        constructions = ConstructionCollection.from_hb_constructions(
            df_model.properties.energy.constructions)

        return cls(df_model.display_name, run_period, polygons=polygons,
                   constructions=constructions, floors=flr_spc)

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

    def to_inp(self):

        data = [
            self._header,
            fb.ttrpddh, self.title.to_inp(),
            self.compliance_data.to_inp(),
            self.site_bldg_data.to_inp(),
            self.constructions.to_inp(),
            fb.polygons,
            '\n'.join(pl.to_inp() for pl in self.polygons),
            fb.wallParams,
            fb.fixBldgShade,
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
