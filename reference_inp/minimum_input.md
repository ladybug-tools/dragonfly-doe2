# Minimum inputs to create a working eQuest *.inp file
***
## eQuest is broken up into what I like to call 'Blocks'
## Each block has it's own formatting
## eQuest confuses the crap out of me sooo... that's part of why so little progress has been made
***
  ```
refer to reference_inp/simple_example.inp
  ```
Preface:<br>
- Nomenclature:
- -  I refer to the 'sections' of the *.inp as 'blocks'<br>
- i.e 'block called 'Title-RP-DD-H' the *header* as I call it seen here:<br>
  ```f#
  $ ---------------------------------------------------------
  $              Title, Run Periods, Design Days, Holidays
  $ ---------------------------------------------------------
  ```
  ^^ Block<br>
-  Intent is to create the corolative 'generic' equivelants / conversions of: df const/sch etc inputs to fulfill all possible eQuest min inputs. Bespoke for eQ as needed 'generic input' wise.
***
1. All block headers required, even if section blank. (F'n fortran lol).
2. where E+ uses ';' to signify end-of-obj strs: eQ user ```'\n   ..'```
3. Fortran is stupid: some of these 'required for file to work' inputs; make no logical sense in terms of 'why without an analysis period is this that and somthing else F'd up'.
***
## File Blocks, block by block in order **if** input required: as above if no input, or no input required: block header still required.
1. file header 
   ```f#
    INPUT ..
   ```
2. Title, Run Periods, Design Days, Holidays:
   - Analysis period required: typical USA users use annual, standard US holidays, library-entry US
  ```f#
   TITLE           
      LINE-1           = *simple_example*
      ..

   "Entire Year" = RUN-PERIOD-PD
      BEGIN-MONTH      = 1
      BEGIN-DAY        = 1
      BEGIN-YEAR       = 2021
      END-MONTH        = 12
      END-DAY          = 31
      END-YEAR         = 2021
      ..


   "Standard US Holidays" = HOLIDAYS        
      LIBRARY-ENTRY "US"
      ..
  ```
3. Compliance Data
  ```f#
    "Compliance Data" = COMPLIANCE      
       C-PERMIT-SCOPE   = 0
       C-PROJ-NAME      = *simple_example*
       C-BUILDING-TYPE  = 0
       C-CONS-PHASE     = 0
       C-NR-DHW-INCL    = 1
       C-CODE-VERSION   = 1
       C-901-NUM-FLRS   = 1
       C-901-BLDG-TYPE  = 32
      ..
  ```
4. Site and Building Data
  ```f#
    "Site Data" = SITE-PARAMETERS 
        ALTITUDE         = 150
        C-STATE          = 21
        C-WEATHER-FILE   = *TMY2\HARTFOCT.bin*
        C-COUNTRY        = 1
        C-901-LOCATION   = 1092
        ..

    "Building Data" = BUILD-PARAMETERS
        HOLIDAYS         = "Standard US Holidays"
        ..



PROJECT-DATA    
   ..
  ```
5. Materials / Layers / Constructions
- see [reference file](/reference_inp/simple_example.inp) line 79 <br>
- solvable via 'use whatever DF uses'. [idf to inp material conversion gist](https://gist.github.com/alnjxn/2591426) intended to be referenced to save time<br>
6. **Glass Types**: refers to stuff in the eQuest lib, not a req just what was used in example; glass mats can be definied in materials / layers /const block
7. Day Schedules block, week schedules block, annual schedules block
   - From what I understand: explicitly required just for geom as geom has some input dependencies i.e programs and stuff, as polys need to be relationed to floors/spaces/walls/windows/doors block which need to be relationed to HVAC Systems / Zones or it doesnt work *rolls eyes*<br>
8. **Polygons** schema is as follows:<br>
  ```
    "floor poly obj"
            |
            V
    "Room1"
        ..
    "Room2"
        ..
    "floor poly 1"
        ..
    *continue*
  ```
- Verts: MUST be: upper_left_counter_clockwise_vertices in poly obj:
  ```f#
    "Floor Polygon" = POLYGON         
     V1               = ( 0, 0 )
     V2               = ( 31.6, 0 )
     V3               = ( 31.6, 31.6 )
     V4               = ( 0, 31.6 )
     ..
  ```
9. Floors / Spaces / Walls / Windows / Doors
- Same schema in terms of:<br>
  ```
    floor1/f1-rm1/f1-rm2 etc
  ```
  Example file in reference_inp uses basic assignment of loads, see privately provided *.inp for switch statement assignment (switch statements are basically naming convention dependant: was the pri for me when this proj was started and focused on the company it was for).
  *Maintaining upper_left_counter_clockwise_vertices* convention: (see privately provided *.inp for detailed reference)<br>
  ```f#
    "Ground Flr" = FLOOR           
       AZIMUTH          = 360
       POLYGON          = "Floor Polygon"
       SHAPE            = POLYGON
       FLOOR-HEIGHT     = 10
       SPACE-HEIGHT     = 8
       C-DIAGRAM-DATA   = *Bldg Envelope & Loads 1 Diag Data*
       C-901-BLDG-TYPE  = 32
       ..
    "Spc (G.1)" = SPACE           
       SHAPE            = POLYGON
       ZONE-TYPE        = UNCONDITIONED
       PEOPLE-SCHEDULE  = "GndFlr Occ Sch"
       LIGHTING-SCHEDUL = ( "GndFlr Ltg Sch" )
       TASK-LIGHT-SCH   = "GndFlr Occ Sch"
       EQUIP-SCHEDULE   = ( "GndFlr Eqp Sch" )
       INF-SCHEDULE     = "GndFlr Sys1 Infil Sch"
       INF-METHOD       = AIR-CHANGE
       INF-FLOW/AREA    = 0.038481
       PEOPLE-HG-LAT    = 158.757
       PEOPLE-HG-SENS   = 245.352
       LIGHTING-W/AREA  = ( 1.108 )
       TASK-LT-W/AREA   = 0.006
       EQUIPMENT-W/AREA = ( 0.524 )
       AREA/PERSON      = 195.694
       POLYGON          = "Floor Polygon"
       C-SCHEDULE-TYPE  = 2
       C-SUB-AREA       = ( 948.63, 29.96, 19.97 )
       C-OCC-TYPE       = ( 24, 35, 18 )
       C-ACTIVITY-DESC  = *Hotel/Motel Guest Room (95%)*
       C-901-OCC-TYPE   = ( 0, 2, 19 )
       C-901-SCH-TYPE   = 1
       C-HTG-SYS-CLASS  = 2
       ..
    "South Wall (G.1.E1)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V1
       ..
    "South Door (G.1.E1.D10)" = DOOR            
       CONSTRUCTION     = "Dbl Lyr Unins Mtl Door"
       X                = 27.8
       HEIGHT           = 6.67
       WIDTH            = 3
       ..
    "East Wall (G.1.E2)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V2
       ..
    "Window 1" = WINDOW          
       GLASS-TYPE       = "Window Type #1 GT"
       X                = 5
       Y                = 2.5
       HEIGHT           = 3
       WIDTH            = 3
       ..
    "North Wall (G.1.E3)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V3
       ..
    "West Wall (G.1.E4)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V4
       ..
    "Ceiling (G.1.I1)" = INTERIOR-WALL   
       NEXT-TO          = "Plnm (G.2)"
       CONSTRUCTION     = "Ceilg Construction"
       LOCATION         = TOP
       ..
    "Flr (G.1.U1)" = UNDERGROUND-WALL
       CONSTRUCTION     = "UFCons (G.1.U2)"
       LOCATION         = BOTTOM
       ..
    "Plnm (G.2)" = SPACE           
       Z                = 8
       HEIGHT           = 2
       SHAPE            = POLYGON
       ZONE-TYPE        = UNCONDITIONED
       INF-SCHEDULE     = "Sys1 (SUM) Inf Sch"
       INF-METHOD       = AIR-CHANGE
       INF-FLOW/AREA    = 0.00962025
       POLYGON          = "Floor Polygon"
       C-SUB-AREA       = ( 998.56 )
       ..
    "South Wall (G.2.E5)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V1
       ..
    "East Wall (G.2.E6)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V2
       ..
    "North Wall (G.2.E7)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V3
       ..
    "West Wall (G.2.E8)" = EXTERIOR-WALL   
       CONSTRUCTION     = "EWall Construction"
       LOCATION         = SPACE-V4
       ..
    "Roof (G.2.E9)" = EXTERIOR-WALL   
       CONSTRUCTION     = "Roof Construction"
       LOCATION         = TOP
       ..
  ```
1.  Finally! HVAC Systems / Zones<br>
  ```f#
      "Sys1 (SUM)" = SYSTEM          
         TYPE             = SUM
         HEAT-SOURCE      = NONE
         SYSTEM-REPORTS   = NO
       ..
      "Zn (G.1)" = ZONE            
         TYPE             = UNCONDITIONED
         DESIGN-HEAT-T    = 72
         DESIGN-COOL-T    = 75
         SIZING-OPTION    = ADJUST-LOADS
         SPACE            = "Spc (G.1)"
       ..
      "Pl Zn (G.2)" = ZONE            
         TYPE             = UNCONDITIONED
         DESIGN-HEAT-T    = 72
         DESIGN-COOL-T    = 75
         SIZING-OPTION    = ADJUST-LOADS
         SPACE            = "Plnm (G.2)"
       ..
  ```
***
## State of affairs:
has currently:
- Polygons
- Floors / Spaces etc blocks* sans walls and windows
***
next steps were to be:<br>
>  refactor to map wall verts with polyverts<br>
>  get windows going<br>
>  likely refactor to make everything properly DF formatted class wise<br>
>  fill in the rest; as that kinda covers most of the important ORMish items
