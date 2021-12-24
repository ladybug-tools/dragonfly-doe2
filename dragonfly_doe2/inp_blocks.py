"""INP text blocks."""

topLevel = 'INPUT ..\n\n\n\n'
spacer = '\n\n'
sd_brk = '$ ---------------------------------------------------------\n'
star_brk = '$ *********************************************************\n'
star_blnk = '$ **                                                     **\n'


abortDiag = '{sd_brk}$              Abort, Diagnostics\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
globalParam = '{sd_brk}$              Global Parameters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
ttrpddh = '{sd_brk}$              Title, Run Periods, Design Days, Holidays\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
comply = '{sd_brk}$              Compliance Data\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
siteBldg = '{sd_brk}$              Site and Building Data\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
matslayers = '{sd_brk}$              Materials / Layers / Constructions\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
glzCode = '{sd_brk}$              Glass Type Codes\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
glzTyp = '{sd_brk}$              Glass Types\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
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
fixBldgShade = '{sd_brk}$              Fixed and Building Shades\n{sd_brk}{spacer}'.format(
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

elecMeter = '{sd_brk}$              Electric Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
fuelMeter = '{sd_brk}$              Fuel Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
masterMeter = '{sd_brk}$              Master Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

hvacCircLoop = star_brk+star_blnk+'$ **      HVAC Circulation Loops / Plant Equipment       **\n'\
    + star_blnk+star_brk+spacer

pumps = '{sd_brk}$              Pumps\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
heatExch = '{sd_brk}$              Heat Exchangers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
circLoop = '{sd_brk}$              Circulation Loops\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
chillyboi = '{sd_brk}$              Chillers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
boilyboi = '{sd_brk}$              Boilers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
dwh = '{sd_brk}$              Domestic Water Heaters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
heatReject = '{sd_brk}$              Heat Rejection\n' + \
    sd_brk+spacer  # allAmericanHeatRejects
towerFree = '{sd_brk}$              Tower Free Cooling\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
pvmod = '{sd_brk}$              Photovoltaic Modules\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
elecgen = '{sd_brk}$              Electric Generators\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
thermalStore = '{sd_brk}$              Thermal Storage\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
groundLoopHx = '{sd_brk}$              Ground Loop Heat Exchangers\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
compDhwRes = sd_brk + \
    '$              Compliance DHW (residential dwelling units)\n' + \
    sd_brk+spacer

steamAndcldMtr = star_brk+star_blnk+'$ **            Steam & Chilled Water Meters             **\n'\
    + star_blnk+star_brk+spacer

steamMtr = '{sd_brk}$              Steam Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
chillMeter = '{sd_brk}$              Chilled Water Meters\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

hvacSysNzone = star_brk+star_blnk+'$ **               HVAC Systems / Zones                  **\n'\
    + star_blnk+star_brk+spacer

miscNmeterHvac = star_brk+star_blnk+'$ **                Metering & Misc HVAC                 **\n'\
    + star_blnk+star_brk+spacer

equipControls = '{sd_brk}$              Equipment Controls\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
loadManage = '{sd_brk}$              Load Management\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

UtilRate = star_brk+star_blnk+'$ **                    Utility Rates                    **\n'\
    + star_blnk+star_brk+spacer

ratchets = '{sd_brk}$              Ratchets\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
blockCharge = '{sd_brk}$              Block Charges\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
utilRate = '{sd_brk}$              Utility Rates\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

outputReporting = star_brk+star_blnk+'$ **                 Output Reporting                    **\n'\
    + star_blnk+star_brk+spacer

loadsNonHr = '{sd_brk}$              Loads Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
sysNonHr = '{sd_brk}$              Systems Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
plntNonHr = '{sd_brk}$              Plant Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
econNonHr = '{sd_brk}$              Economics Non-Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)
hourlyRep = '{sd_brk}$              Hourly Reporting\n{sd_brk}{spacer}'.format(
    sd_brk=sd_brk, spacer=spacer)

theEnd = '{sd_brk}$              THE END\n' + \
    sd_brk+'\nEND ..\nCOMPUTE ..\nSTOP ..\n'
