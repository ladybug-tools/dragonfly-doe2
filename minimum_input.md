# Minimum inputs to create a working eQuest *.inp file
***
## eQuest is broken up into what I like to call 'Blocks'
## Each block has it's own formatting
***
```
refer to reference_inp/simple_example.inp
```
Preface:<br>
- Nomenclature:
- -  I refer to the 'sections' of the *.inp as 'blocks'<br>
- i.e 'block called 'Title-RP-DD-H' the *header* as I call it seen here:<br>
```
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
   ```
   INPUT ..
   ```
2. Title, Run Periods, Design Days, Holidays:
   - Analysis period required: typical USA users use annual, standard US holidays, library-entry US
```
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
```
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
```
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
1. Floors / Spaces / Walls / Windows / Doors
- Same schema in terms of:<br>
  ```
  floor1/f1-rm1/f1-rm2 etc
  ```
  Example file in reference_inp uses basic assignment of walls and loads, see privately provided *.inp for switch statement assignment (switch statements are basically naming convention dependant: was the pri for me when this proj was started and focused on the company it was for).
  - example file in reference_inp uses 'wizzard schema' for wall assignment facilitated by the 'template building shapes' in eQuest, otherwise would be assigned (in our application) as follow:<br>
  *Maintaining upper_left_counter_clockwise_vertices* convention: (see privately provided *.inp for detailed reference)<br>
    ```
  "Breakroom-1_L1_SP" = SPACE           
     SHAPE            = POLYGON
     SOURCE-SCHEDULE  = {#L("PEOPLE-SCHEDULE")}
     SOURCE-TYPE      = PROCESS
     SOURCE-POWER     = {#L("AREA")/#L("AREA/PERSON")*(450-350)}
     NUMBER-OF-PEOPLE = 0
     POLYGON          = "Breakroom-1_L1 Plg"
     C-ACTIVITY-DESC  = *brkm*
     ..
  "Exterior Wall 104" = EXTERIOR-WALL   
     LOCATION         = SPACE-V1
     ..
  "Window 1" = WINDOW          
     X                = 0.5
     HEIGHT           = {13.5*#pa("WWR_adj")}
     WIDTH            = 4
     ..
  "Exterior Wall 105" = EXTERIOR-WALL   
     LOCATION         = SPACE-V2
     ..
  "Window 2" = WINDOW          
     X                = 7.25
     HEIGHT           = {13.5*#pa("WWR_adj")}
     WIDTH            = 4
     ..
  "Exterior Wall 106" = EXTERIOR-WALL   
     LOCATION         = SPACE-V3
     ..
  "Window 3" = WINDOW          
     X                = 0.5
     HEIGHT           = {13.5*#pa("WWR_adj")}
     WIDTH            = 4
     ..
  "Exterior Wall 107" = EXTERIOR-WALL   
     LOCATION         = SPACE-V4
     ..
  "Window 4" = WINDOW          
     X                = 7.25
     HEIGHT           = {13.5*#pa("WWR_adj")}
     WIDTH            = 4
     ..
  "Exterior Wall 108" = EXTERIOR-WALL   
     LOCATION         = SPACE-V5
     ..
  "Window 5" = WINDOW          
     X                = 0.5
     HEIGHT           = {13.5*#pa("WWR_adj")}
     WIDTH            = 4
     ..
    ```
            