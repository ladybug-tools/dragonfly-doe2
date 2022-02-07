"""INP text blocks."""

top_level = 'INPUT ..\n\n\n\n'
spacer = '\n\n'
sd_brk = '$ ---------------------------------------------------------\n'
star_brk = '$ *********************************************************\n'
star_blnk = '$ **                                                     **\n'


abort_diag = '{sd_brk}$              Abort, Diagnostics\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
global_params = '{sd_brk}$              Global Parameters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
ttrpddh = '{sd_brk}$              Title, Run Periods, Design Days, Holidays\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
comply = '{sd_brk}$              Compliance Data\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
mats_layers = '{sd_brk}$              Materials / Layers / Constructions\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
glzCode = '{sd_brk}$              Glass Type Codes\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
glzTyp = '{sd_brk}$              Glass Types\n{sd_brk}{spacer}\n\n'.format(
    sd_brk=sd_brk, spacer=spacer) +\
    '"WT1" = GLASS-TYPE\n  '\
    'TYPE             = GLASS-TYPE-CODE\n   '\
    'GLASS-TYPE-CODE  = "2001"\n   '\
    'C-PRODUCT-TYPE   = 0\n   '\
    'C-FRAME-TYPE     = 0\n   '\
    '..\n\n'
WindowLayers = '{sd_brk}$              Window Layers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
iLikeLamp = '{sd_brk}$              Lamps / Luminaries / Lighting Systems\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
daySch = '{sd_brk}$              Day Schedules\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
weekSch = '{sd_brk}$              Week Schedules\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
annualSch = '{sd_brk}$              Annual Schedules\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
polygons = '{sd_brk}$              Polygons\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
wallParams = spacer+'{sd_brk}$              Wall Parameters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
fix_bldg_shade = '{sd_brk}$              Fixed and Building Shades\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
miscCost = '{sd_brk}$              Misc Cost Related Objects\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)


perfCurve = star_brk+star_blnk+'$ **                Performance Curves                   **\n'\
    + star_blnk+star_brk+spacer
floorNspace = star_brk+star_blnk+'$ **      Floors / Spaces / Walls / Windows / Doors      **\n'\
    + star_blnk+star_brk+spacer
elecFuelMeter = spacer+star_brk+star_blnk + \
    '$ **              Electric & Fuel Meters                 **\n' + \
    star_blnk+star_brk+spacer

elec_meter = '{sd_brk}$              Electric Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
fuel_meter = '{sd_brk}$              Fuel Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
master_meter = '{sd_brk}$              Master Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

hvac_circ_loop = star_brk+star_blnk+'$ **      HVAC Circulation Loops / Plant Equipment       **\n'\
    + star_blnk+star_brk+spacer

pumps = '{sd_brk}$              Pumps\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
heat_exch = '{sd_brk}$              Heat Exchangers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
circ_loop = '{sd_brk}$              Circulation Loops\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
chiller_objs = '{sd_brk}$              Chillers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
boiler_objs = '{sd_brk}$              Boilers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
dwh = '{sd_brk}$              Domestic Water Heaters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
heat_reject = '{sd_brk}$              Heat Rejection\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk,
    spacer=spacer)
tower_free = '{sd_brk}$              Tower Free Cooling\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
pvmod = '{sd_brk}$              Photovoltaic Modules\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
elecgen = '{sd_brk}$              Electric Generators\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
thermal_store = '{sd_brk}$              Thermal Storage\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
ground_loop_hx = '{sd_brk}$              Ground Loop Heat Exchangers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
comp_dhw_res = sd_brk + \
    '$              Compliance DHW (residential dwelling units)\n' + \
    sd_brk+spacer

steam_cld_mtr = star_brk+star_blnk+'$ **            Steam & Chilled Water Meters             **\n'\
    + star_blnk+star_brk+spacer

steam_mtr = '{sd_brk}$              Steam Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
chill_meter = '{sd_brk}$              Chilled Water Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

hvac_sys_zone = star_brk+star_blnk+'$ **               HVAC Systems / Zones                  **\n'\
    + star_blnk+star_brk+spacer

misc_meter_hvac = star_brk+star_blnk+'$ **                Metering & Misc HVAC                 **\n'\
    + star_blnk+star_brk+spacer

equip_controls = '{sd_brk}$              Equipment Controls\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
load_manage = '{sd_brk}$              Load Management\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

big_util_rate = star_brk+star_blnk+'$ **                    Utility Rates                    **\n'\
    + star_blnk+star_brk+spacer

ratchets = '{sd_brk}$              Ratchets\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
block_charge = '{sd_brk}$              Block Charges\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
small_util_rate = '{sd_brk}$              Utility Rates\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

output_reporting = star_brk+star_blnk+'$ **                 Output Reporting                    **\n'\
    + star_blnk+star_brk+spacer

loads_non_hrly = '{sd_brk}$              Loads Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
sys_non_hrly = '{sd_brk}$              Systems Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
plant_non_hrly = '{sd_brk}$              Plant Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
econ_non_hrly = '{sd_brk}$              Economics Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
hourly_rep = '{sd_brk}$              Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

the_end = '{sd_brk}$              THE END\n{sd_brk}'.format(
    sd_brk=sd_brk) + '\nEND ..\nCOMPUTE ..\nSTOP ..\n'
