

topLevel = 'INPUT ..\n\n\n\n'
spacer = '\n\n'
sd_brk = '$ ---------------------------------------------------------\n'
abortDiag = sd_brk + '$              Abort, Diagnostics\n' + sd_brk + spacer
globalParam = sd_brk + '$              Global Parameters\n'+sd_brk+spacer
ttrpddh = sd_brk+'$              Title, Run Periods, Design Days, Holidays\n'+sd_brk+spacer
comply = sd_brk+'$              Compliance Data\n'+sd_brk+spacer
siteBldg = sd_brk+'$              Site and Building Data\n'+sd_brk+spacer
matslayers = sd_brk+'$              Materials / Layers / Constructions\n'+sd_brk+spacer
glzCode = sd_brk+'$              Glass Type Codes\n'+sd_brk+spacer
glzTyp = sd_brk+'$              Glass Types\n'+sd_brk+spacer
WindowLayers = sd_brk+'$              Window Layers\n'+sd_brk+spacer
iLikeLamp = sd_brk+'$              Lamps / Luminaries / Lighting Systems\n'+sd_brk+spacer
daySch = sd_brk+'$              Day Schedules\n'+sd_brk+spacer
weekSch = sd_brk+'$              Week Schedules\n'+sd_brk+spacer
annualSch = sd_brk+'$              Annual Schedules\n'+sd_brk+spacer
polygons = sd_brk+'$              Polygons\n'+sd_brk+spacer
wallParams = spacer+sd_brk+'$              Wall Parameters\n'+sd_brk+spacer
fixBldgShade = sd_brk+'$              Fixed and Building Shades\n'+sd_brk+spacer
miscCost = sd_brk+'$              Misc Cost Related Objects\n'+sd_brk+spacer

star_brk = '$ *********************************************************\n'
star_blnk = '$ **                                                     **\n'

perfCurve = star_brk+star_blnk+'$ **                Performance Curves                   **\n'\
    + star_blnk+star_brk+spacer
floorNspace = star_brk+star_blnk+'$ **      Floors / Spaces / Walls / Windows / Doors      **\n'\
    + star_blnk+star_brk+spacer
elecFuelMeter = spacer+star_brk+star_blnk + \
    '$ **              Electric & Fuel Meters                 **\n' + \
    star_blnk+star_brk+spacer

elecMeter = sd_brk+'$              Electric Meters\n'+sd_brk+spacer
fuelMeter = sd_brk+'$              Fuel Meters\n'+sd_brk+spacer
masterMeter = sd_brk+'$              Master Meters\n'+sd_brk+spacer

hvacCircLoop = star_brk+star_blnk+'$ **      HVAC Circulation Loops / Plant Equipment       **\n'\
    + star_blnk+star_brk+spacer

pumps = sd_brk+'$              Pumps\n'+sd_brk+spacer
heatExch = sd_brk+'$              Heat Exchangers\n'+sd_brk+spacer
circLoop = sd_brk+'$              Circulation Loops\n'+sd_brk+spacer
chillyboi = sd_brk+'$              Chillers\n'+sd_brk+spacer
boilyboi = sd_brk+'$              Boilers\n'+sd_brk+spacer
dwh = sd_brk+'$              Domestic Water Heaters\n'+sd_brk+spacer
heatReject = sd_brk+'$              Heat Rejection\n' + \
    sd_brk+spacer  # allAmericanHeatRejects
towerFree = sd_brk+'$              Tower Free Cooling\n'+sd_brk+spacer
pvmod = sd_brk+'$              Photovoltaic Modules\n'+sd_brk+spacer
elecgen = sd_brk+'$              Electric Generators\n'+sd_brk+spacer
thermalStore = sd_brk+'$              Thermal Storage\n'+sd_brk+spacer
groundLoopHx = sd_brk+'$              Ground Loop Heat Exchangers\n'+sd_brk+spacer
compDhwRes = sd_brk + \
    '$              Compliance DHW (residential dwelling units)\n' + \
    sd_brk+spacer

steamAndcldMtr = star_brk+star_blnk+'$ **            Steam & Chilled Water Meters             **\n'\
    + star_blnk+star_brk+spacer

steamMtr = sd_brk+'$              Steam Meters\n'+sd_brk+spacer
chillMeter = sd_brk+'$              Chilled Water Meters\n'+sd_brk+spacer

hvacSysNzone = star_brk+star_blnk+'$ **               HVAC Systems / Zones                  **\n'\
    + star_blnk+star_brk+spacer

miscNmeterHvac = star_brk+star_blnk+'$ **                Metering & Misc HVAC                 **\n'\
    + star_blnk+star_brk+spacer

equipControls = sd_brk+'$              Equipment Controls\n'+sd_brk+spacer
loadManage = sd_brk+'$              Load Management\n'+sd_brk+spacer

UtilRate = star_brk+star_blnk+'$ **                    Utility Rates                    **\n'\
    + star_blnk+star_brk+spacer

ratchets = sd_brk+'$              Ratchets\n'+sd_brk+spacer
blockCharge = sd_brk+'$              Block Charges\n'+sd_brk+spacer
utilRate = sd_brk+'$              Utility Rates\n'+sd_brk+spacer

outputReporting = star_brk+star_blnk+'$ **                 Output Reporting                    **\n'\
    + star_blnk+star_brk+spacer

loadsNonHr = sd_brk+'$              Loads Non-Hourly Reporting\n'+sd_brk+spacer
sysNonHr = sd_brk+'$              Systems Non-Hourly Reporting\n'+sd_brk+spacer
plntNonHr = sd_brk+'$              Plant Non-Hourly Reporting\n'+sd_brk+spacer
econNonHr = sd_brk+'$              Economics Non-Hourly Reporting\n'+sd_brk+spacer
hourlyRep = sd_brk+'$              Hourly Reporting\n'+sd_brk+spacer

theEnd = sd_brk+'$              THE END\n' + \
    sd_brk+'\nEND ..\nCOMPUTE ..\nSTOP ..\n'
