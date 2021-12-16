# Boundary Conditions:
## BC's are assigned in *.inp file in block
```f#
    $ *********************************************************
    $ **                                                     **
    $ **      Floors / Spaces / Walls / Windows / Doors      **
    $ **                                                     **
    $ *********************************************************
```
-  Using Privately shared model as reference:<br>
  **Underground Wall**
    ```f#
        "Mechanical-2_L-1_SP" = SPACE           
            SHAPE            = POLYGON
            POLYGON          = "Mechanical-2_L-1 Plg"
            C-ACTIVITY-DESC  = *mech*
            ..
         "Mechanical-2_L-1_SOG" = UNDERGROUND-WALL
            LOCATION         = BOTTOM
            ..
         "Underground Wall 35" = UNDERGROUND-WALL
            HEIGHT           = 22
            LOCATION         = SPACE-V1
            ..
         "Underground Wall 36" = UNDERGROUND-WALL
            HEIGHT           = 22
            LOCATION         = SPACE-V2
            ..
         "Underground Wall 37" = UNDERGROUND-WALL
            HEIGHT           = 22
            LOCATION         = SPACE-V3
            ..
    ```
-  **Underground Roof/Ceiling**
    ```f#
        "Animal Holding-2_L-1_SP" = SPACE           
            SHAPE            = POLYGON
            POLYGON          = "Animal Holding-2_L-1 Plg"
            C-ACTIVITY-DESC  = *hold*
            ..
         "Animal Holding-2_L-1_SOG" = UNDERGROUND-WALL
            LOCATION         = BOTTOM
            ..
    ```
-  **Above Ground walls / Ceiling adjacent to off-set inboard; higher story**
    ```f#
        "Corridor-3_L2_SP" = SPACE           
            SHAPE            = POLYGON
            SOURCE-SCHEDULE  = {#L("PEOPLE-SCHEDULE")}
            SOURCE-TYPE      = PROCESS
            SOURCE-POWER     = {#L("AREA")/#L("AREA/PERSON")*(450-350)}
            NUMBER-OF-PEOPLE = 0
            POLYGON          = "Corridor-3_L2 Plg"
            C-ACTIVITY-DESC  = *corr*
            ..
         "Corridor-3_L2_IW" = INTERIOR-WALL   
            NEXT-TO          = "Corridor-3_L2_Dmy_SP"
            CONSTRUCTION     = "Default Air Wall Construction"
            LOCATION         = TOP
            ..
   ```
<img src=".reference_inp/rsrcs/abv_grd_clg.jpg">
