extensions[gis]

breed [vertices vertex]   ;;the nodes
breed [commuters commuter]  ;;people
breed [nodes node]  ;;nodes representing people in networks

globals [
  world-size
  gmu-buildings
  gmu-roads
  gmu-walkway
  gmu-lakes
  gmu-rivers
  gmu-drive
  got_to_destination    ;;count the total number of arrivals
  homes
  works
  hour
  minute
]

patches-own[
  centroid? ;;is it the centroid of a building?
  id   ;;if it is a centroid of a building, it has an ID that represents the building
  entrance ;;nearest vertex on road. only for centroids.
  function ;; 1 for work, 2 for home, 0 for neither
]

commuters-own [
  mynode  ;;a vertex. where he begins his trip
  destination  ;;the destination he wants to arrive at
  destination-entrance  ;;the entrance of the destination on the road
  mypath   ;;an agentset containing nodes to visit in the shortest path
  step-in-path  ;;the number of step taking in the walk
  last-stop ;;last destination
  Myhome  ;;home location
  Mywork  ;;work location
  start_time_h  ;;time to start going to work, hour and minute
  start_time_m
  end_time_h  ;;time to leave work, hour and minute
  end_time_m
  home_friends  ;;list of friends at home
  work_friends ;;list of friends at work
  num_friends  ;;number of friends
  status;; work, home, or transport
  testing  ;;a temp variable used in identifying friends
  happiness_home
  happiness_work
  commuter_id   ;used to link commuters and nodes
]

vertices-own [
  myneighbors  ;;agentset of neighboring vertices
  entrance?  ;;if it is an entrance to a building
  test  ;;used to delete in test

  ;;the follwoing variables are used and renewed in each path-selection
  dist  ;;distance from original point to here
  done ;;1 if has calculated the shortest path through this point, 0 otherwise
  lastnode ;;last node to this point in shortest path
]

nodes-own [
  node_id
]

links-own [
  friend_type
]

to setup
  ca
  reset-ticks

  ;;loading GIS files here
  set gmu-buildings gis:load-dataset "../data/raw/gmu/Mason_bld.shp"
  set gmu-walkway gis:load-dataset "../data/raw/gmu/Mason_walkway_line.shp"
  set world-size gis:load-dataset "../data/raw/gmu/world.shp"
  gis:set-world-envelope gis:envelope-of world-size
  ;;gis:set-world-envelope gis:envelope-of gmu-walkway

  gis:set-drawing-color 5 gis:fill gmu-buildings 1.0

  if show_lakes? [
    set gmu-lakes gis:load-dataset "../data/raw/gmu/hydrop.shp"
    set gmu-rivers gis:load-dataset "../data/raw/gmu/hydrol.shp"
    gis:set-drawing-color 87 gis:fill gmu-lakes 1.0
    gis:set-drawing-color 87 gis:draw gmu-rivers 0.5
  ]

  if show_driveway? [
    set gmu-drive gis:load-dataset "../data/raw/gmu/Mason_Rds.shp"
    gis:set-drawing-color 36 gis:fill gmu-drive 1.0
  ]

  ;gis:set-drawing-color 25  gis:draw gmu-walkway 1.0

  ;identify centroids and assign IDs to centroids
  foreach gis:feature-list-of gmu-buildings [ building ->
    let center-point gis:location-of gis:centroid-of building
    ask patch item 0 center-point item 1 center-point [
      set centroid? true
      set id gis:property-value building "Id"
      set function gis:property-value building "function"
      if function = nobody [set function 0]  ;;deal with no data
    ]
  ]

  ;;ask patches with [ centroid? = true][sprout 1 [set size 2 set color red]] ;;use this line to verify

  ;;create turtles representing the nodes. create links to conect them.
  foreach gis:feature-list-of gmu-walkway [ road-feature ->
    foreach gis:vertex-lists-of road-feature [ v ->  ; for the road feature, get the list of vertices
      let previous-node-pt nobody
      foreach v [ n ->  ; for each vertex in road segment feature
        let location gis:location-of n
        if not empty? location [
          ;ifelse any? vertices with [(xcor = item 0 location and ycor = item 1 location) ] ; if there is not a road-vertex here already
          create-vertices 1 [
            set myneighbors n-of 0 turtles ;;empty
            set xcor item 0 location
            set ycor item 1 location
            set size 0.2
            set shape "circle"
            set color brown
            set hidden? true

            ; create link to previous node
            ifelse previous-node-pt = nobody
              [] ; first vertex in feature
              [create-link-with previous-node-pt] ; create link to previous node
            set previous-node-pt self
          ]
        ]
      ]
    ]
  ]

  ;;delete duplicate vertices (there may be more than one vertice on the same patch due to reducing size of the map). therefore, this map is simplified from the original map.
  delete-duplicates

  ;;delete some nodes not connected to the network
  ask vertices [set myneighbors link-neighbors]
  delete-not-connected
  ask vertices [set myneighbors link-neighbors]

  ;;find nearest node to become entrance
  ask patches with [centroid? = true] [
    set entrance min-one-of vertices in-radius 50 [distance myself]
    ask entrance [set entrance? true]
    if show_nodes? [ask vertices [set hidden? false]]
    if show_entrances? [ask entrance [set hidden? false set shape "star" set size 0.5]]
  ]

  set got_to_destination 0

  ;;verification
  ;;ask one-of vertices [set hidden? false set color red ask myneighbors [set hidden? false set color yellow]]

  ask links [set thickness 0.1 set color orange]

  ;;set up homes and work places
  set works patches with [centroid? = true and function = 1]
  set homes patches with [centroid? = true and function = 2]

  create-the-commuters

  set hour 6
  set minute 0

  ;;set up networks
  create-nodes number-of-commuters [
    set color yellow
    set node_id who - count commuters
    move-to one-of patches with [pxcor > 45 and count turtles-here < 1]
  ]
end

to move
  ;;setting the clock
  set minute minute + 5
  if minute = 60 [
    ifelse hour = 23
      [set hour 0]
      [set hour hour + 1]
    set minute 0
  ]

  ;;checking happiness
  ask commuters with [status = "work"] [
    ifelse (count work_friends > max_friends)
    [
      set happiness_work happiness_work - decrease * (count work_friends - max_friends)
    ]
    [
      ifelse (count work_friends < min_friends)
        [set happiness_work happiness_work - decrease * ( min_friends - count work_friends)]
        [set happiness_work happiness_work + increase]
    ]
    if happiness_work < 0 [relocate_work]
  ]

  ask commuters with [status = "home"] [
    ifelse (count home_friends > max_friends)
    [
      set happiness_home happiness_home - decrease * (count home_friends - max_friends)
    ]
    [
      ifelse (count home_friends < min_friends)
        [set happiness_home happiness_home - decrease * ( min_friends - count home_friends)]
        [set happiness_home happiness_home + increase]
    ]
    if happiness_home < 0 [relocate_home]
  ]

  ;;start going to work
  ask commuters with [status = "home" and hour = start_time_h and minute = start_time_m] [
    set mynode min-one-of vertices [distance myself]
    move-to mynode ;;move to nearest road
    set destination mywork
    set destination-entrance [entrance] of destination
    ;while [destination-entrance = mynode] [set destination one-of patches with [centroid? = true] set destination-entrance [entrance] of destination]

    ;;select shortest path
    path-select
    set status "transport"
  ]

  ;;start going home
  ask commuters with [status = "work" and hour = end_time_h and minute = end_time_m] [
    set mynode min-one-of vertices [distance myself]
    move-to mynode ;;move to nearest road
    set destination myhome
    set destination-entrance [entrance] of destination
    ;while [destination-entrance = mynode] [set destination one-of patches with [centroid? = true] set destination-entrance [entrance] of destination]

    ;;select shortest path
    path-select
    set status "transport"
  ]

  ;;move along the path selected
  ask commuters with [status = "transport"] [
    ;ifelse xcor != [xcor] of destination-entrance or ycor != [ycor] of destination-entrance [
    ifelse distance destination-entrance > 0.5
    [
      let next_node item step-in-path mypath
      let dist1 distance next_node
      let remain speed
      while [remain > dist1 and step-in-path < length mypath] [
        move-to next_node
        set step-in-path step-in-path + 1
        set remain remain - dist1
        ifelse step-in-path < length mypath
          [
            set next_node item step-in-path mypath
          ]
          [
            set remain 0
            move-to destination
            if destination = mywork [set status "work"]
            if destination = myhome [set status "home"]
            set got_to_destination got_to_destination + 1
          ]  ;;it has reached destination
        set dist1 distance next_node
      ]
      face next_node fd remain
    ]
    [ ;move-to destination
      move-to destination
      if destination = mywork [set status "work"]
      if destination = myhome [set status "home"]

      set got_to_destination got_to_destination + 1
    ]  ;;arrive and start to work
  ]

  ;;make friends at work. each tick there is a x% chance to make a new friend
  ask commuters with [status = "work"] [
    ask work_friends [set testing 1]
    let non-friends count commuters-here with [testing = 0]  ;;one that is not a friend yet
    if non-friends > 0 and random-float 1 < chance_new_friend [
      let target_friend one-of commuters-here with [testing = 0]
      ask target_friend [
        set work_friends (turtle-set work_friends myself)
      ]
      set work_friends (turtle-set work_friends target_friend)
    ]
    ask work_friends [set testing 0]
  ]

  visualize-networks
  tick
end


;;;;;;;;;;;;;;;;;helper functions;;;;;;;;;;;;;;;;;;;;;;;;;;

to create-the-commuters
  create-commuters number-of-commuters [
    set commuter_id who
    set color white
    set size 0.5
    set shape "person"
    set destination nobody
    set last-stop nobody
    ;;set mynode one-of vertices move-to mynode
    set myhome one-of homes
    set mywork one-of works
    move-to myhome
    set status "home"
    set start_time_h round(random-normal 6.5 1)
    ;;will start going to work between 6 and 9
    while [start_time_h < 6 or start_time_h > 9] [
      set start_time_h round(random-normal 6.5 1)
    ]
    set start_time_m (random 12) * 5
    set end_time_h start_time_h + 8  ;will work for 8 hours
    set end_time_m start_time_m
    set happiness_work 100
    set happiness_home 100
    set work_friends commuters with [happiness_home < -99999]  ;;empty set
  ]

  ask commuters [set home_friends commuters-here]
end

to delete-duplicates
  ask vertices [
    if count vertices-here > 1 [
      ask other vertices-here [
        ask myself [create-links-with other [link-neighbors] of myself]
        die
      ]
    ]
  ]
end

to delete-not-connected
  ask vertices [set test 0]
  ask one-of vertices [set test 1]
  repeat 500 [
    ask vertices with [test = 1]
    [ask myneighbors [set test 1]]
  ]
  ask vertices with [test = 0] [die]
end

to relocate_home
  let old_home myhome
  while [myhome = old_home] [set myhome one-of homes]
  set home_friends commuters with [myhome = [myhome] of myself]
  set happiness_home 100
end

to relocate_work
  let old_work mywork
  while [mywork = old_work] [set mywork one-of works]
  set work_friends commuters with [happiness_work < -99999] ;;empty agent set
  ;;set work_friends nobody
  set happiness_work 100
end

to path-select
  ;;use the A-star algorithm to find the shortest path (shortest in terms of distance)
  set mypath []
  set step-in-path 0

  ask vertices [
    set dist 99999
    set done 0
    set lastnode nobody
    set color brown
  ]

  ask mynode [set dist 0] ;;distance to original node is 0

  while [count vertices with [done = 0] > 0] [
    ask vertices with [dist < 99999 and done = 0] [
      ask myneighbors [
        let dist0 distance myself + [dist] of myself    ;;renew the shorstest distance to this point if it is smaller
        if dist > dist0 [
          set dist dist0
          set done 0 ;;done=0 if dist renewed, so that it will renew the dist of its neighbors
          set lastnode myself
        ]  ;;record the last node to reach here in the shortest path
        ;set color red  ;;all roads searched will get red
      ]
      set done 1  ;;set done 1 when it has renewed it neighbors
    ]
  ]

  ;print "Found path"

  ;;put nodes in shortest path into a list
  let x destination-entrance

  while [x != mynode] [
    ; if show_path? [ask x [set color yellow] ] ;;highlight the shortest path
    set mypath fput x mypath
    set x [lastnode] of x
  ]
end

to plot_bins_work
  if ticks > 0 [
    clear-plot
    ;set-histogram-num-bars length all_counts
    ask commuters [set num_friends count work_friends]
    histogram [num_friends] of commuters
  ]
end

to plot_bins_home
  if ticks > 0 [
    clear-plot
    ;set-histogram-num-bars length all_counts
    ask commuters [set num_friends count home_friends]
    histogram [num_friends] of commuters
  ]
end

to visualize-networks
  clear-links
  ask commuters with [count work_friends > 0] [
    let friend_nodes nodes with [node_id > 99999] ;;empty set

    ask work_friends with [commuter_id != [commuter_id] of myself][
      let new nodes with [node_id = [commuter_id] of myself]
      set friend_nodes (turtle-set friend_nodes  new)
    ]

    ask nodes with [node_id = [commuter_id] of myself] [
      create-links-with friend_nodes [set color blue]
    ]
  ]

  ask commuters with [count home_friends > 0] [
    let friend_nodes nodes with [node_id > 99999] ;;empty set

    ask home_friends with [commuter_id != [commuter_id] of myself] [
      let new nodes with [node_id = [commuter_id] of myself]
      set friend_nodes (turtle-set friend_nodes  new)
    ]

    ask nodes with [node_id = [commuter_id] of myself] [
      create-links-with friend_nodes  [set color red]
    ]
  ]
end
@#$#@#$#@
GRAPHICS-WINDOW
259
29
1067
438
-1
-1
10.0
1
10
1
1
1
0
0
0
1
0
79
0
39
0
0
1
ticks
30.0

BUTTON
30
19
93
52
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
31
256
203
289
number-of-commuters
number-of-commuters
10
200
109.0
1
1
NIL
HORIZONTAL

BUTTON
99
18
162
51
NIL
move
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
173
19
236
52
Go
move
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SWITCH
1663
741
1833
774
show_entrances?
show_entrances?
0
1
-1000

SWITCH
1663
697
1832
730
show_nodes?
show_nodes?
0
1
-1000

TEXTBOX
1667
773
1817
801
Entrances will be shown as star shape.
11
0.0
1

SWITCH
1468
679
1641
712
show_lakes?
show_lakes?
0
1
-1000

SWITCH
1469
724
1640
757
show_driveway?
show_driveway?
0
1
-1000

TEXTBOX
1457
386
1607
442
1 tick = 5min
11
0.0
1

MONITOR
265
35
322
80
Hour
hour
17
1
11

MONITOR
326
35
383
80
Minute
minute
17
1
11

TEXTBOX
268
388
418
430
Key:\nRed Lines: Home Friends\nBlue Lines: Work Friends
11
50.0
0

PLOT
42
454
404
670
Status
Time
No. of Commuters
0.0
10.0
0.0
10.0
true
true
"" ""
PENS
"Home" 1.0 0 -2674135 true "" "plot count commuters with [status = \"home\"]"
"Work" 1.0 0 -13345367 true "" "plot count commuters with [status = \"work\"]"
"Traveling" 1.0 0 -7500403 true "" "plot count commuters with [status = \"transport\"]"

SLIDER
29
373
201
406
chance_new_friend
chance_new_friend
0
100
5.0
0.1
1
NIL
HORIZONTAL

PLOT
1373
117
1610
326
Number of friendships
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"" 1.0 0 -16777216 true "" "plot ((sum [count home_friends] of commuters) + (sum [count work_friends] of commuters) )/ 2"

SLIDER
29
300
201
333
speed
speed
0
10
2.0
1
1
NIL
HORIZONTAL

TEXTBOX
34
337
209
365
Agents move x patches per 5 min
11
0.0
1

TEXTBOX
48
416
198
444
Percent chance to make a new friend every 5 min
11
0.0
1

INPUTBOX
38
84
114
144
min_friends
5.0
1
0
Number

INPUTBOX
121
84
207
144
max_friends
10.0
1
0
Number

TEXTBOX
33
63
228
91
No. of friends needed to be happy
11
0.0
1

PLOT
747
457
1069
672
Friends at work
No. of friends at work
Count of People
0.0
30.0
0.0
50.0
true
false
"" ""
PENS
"default" 1.0 1 -16777216 false "" "plot_bins_work"

INPUTBOX
31
188
113
248
increase
0.5
1
0
Number

TEXTBOX
30
154
242
182
Ratio - how much happiness will change per tick
11
0.0
1

INPUTBOX
120
188
199
248
decrease
0.5
1
0
Number

PLOT
416
456
739
672
Firends at Home
No. of friends at home
Count of people
0.0
30.0
0.0
50.0
true
false
"" ""
PENS
"default" 1.0 1 -16777216 false "" "plot_bins_home"

@#$#@#$#@
## WHAT IS IT?

This is a path-finding model using the A-star algorithm to find the shortest path. The models uses the map of George Mason University, including the buildings, walkways, drive-ways, and waters. Commuters randomly select a building as destination, find and follow the shortest path to reach there.

The following is the original map this model uses. It has been simplified in the model for faster computation.

![Picture not found](file:data/Mason.jpg)

## HOW IT WORKS

In the beginning, each commuter randomly selects a destination and then identify the shortest path to the destination. The A-star algorithm is used to find the shortest path in terms of distance. The commuters move one node in a tick. When they reach the destination, they stay there for one tick, and then find the next destination and move again.

## HOW TO USE IT

1. Create a certain number of commuters using the slider.
2. Adjust the settings (switches) as needed.
2. Press mvoe to run the program.
3. For verification, turn "show_path?" on, and create only one commuter. Press move one at a time and observe his movement step by step.

## THINGS TO NOTICE

You may want to turn off some layers for a clear display.

## THINGS TO TRY

Change the switches for different dispalys. Try different number of coimmuters. Try the verification.

## EXTENDING THE MODEL

What if the commuters move with a speed (some distance per tick) instead of one node per tick?

## NETLOGO FEATURES

For faster compuation, this model simplifies the original data by reducing the number of nodes. To do that, the walkway data is loaded to the 20 x 20 grid in Netlogo, which is small, and therefore, many nodes fall on the same patch. In each patch, we only want to keep one node, and duplicate nodes are removed, while their neighbors are connected to the one node left.

Also, links are created in this model to represent raods. This is so far the best way I can find to deal with road related problems in Netlogo. However, because the way I create links is to link nodes one by one (see code for more details), so some roads are likely to be left behind. But again there is no better way I can find. Therefore, I also used a loop in setup to delete nodes that are not connected to the whole network.

## RELATED MODELS

Reston commuters model by Melanie Swartz

## CREDITS AND REFERENCES

The way of creating roading using links is inpired by the Reston commuters model by Melanie Swartz
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.2.1
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
