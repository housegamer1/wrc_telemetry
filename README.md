# Simple Python EA Sports WRC Telemetry Client

Just a little free time fun project, don't expect too much 😊<br>
Made to run in Windows CMD (works in git bash though, did not try Linux. IO will probably crash there)<br>
Made in python 3.<br>
Runs without Simhub.<br><br>

Might develop some more on this, let me know if you come across any issues.

## Features

* Display UDP info provided by EA Sports WRC in a dashboard view for the windows commandline
* Optionally show throttle & brake input as a graph, as well as an accelerometer graph (see known issues)
* Display suspension travel
* Record and replay telemetry data (can skip forward in replays with right arrow key)

Dashboard and Dashboard + Graphs is intentionally kept separate, as the graphs take up quite a lot of screenspace, and which might not be the most practical in case you want to capture the window on top of your game footage.

```
(1) Dashboard | (2) Dashboard + Graphs | (3) Suspension | (4) Raw | (Q) Quit | (R) Record/Stop | (L) Load

>>>   Throttle:         [===========]   >>>   Brake:            [           ]
>>>   Clutch:           [           ]   >>>   Handbrake:        [           ]

>>>   Distance:         1.18/7.98 km    >>>   Steering:         [          =          ]

>>>   Gear:             1/6             >>>   RPM:              [===========]   8341/8700
>>>   Gps Speed:        54 Km/h         >>>   Trans Speed:      66 Km/h
>>>   Brake Temp:       FL [||] 332      FR [||] 310
                        RL [||] 327      RR [||] 299

>>>   Histo:             _____________________  >>>   Accel:    Fw: -0.1g (max: -1.1) Sw: -0.5g (max: 1.9)
                       /_                                       ..............................
                      /                                         ..............................
                   /__                                          ..............................
                 /_                                             ..............................
                _                                               ...........--.................
                                                                ...........-+.................
                                                                ..............................
                                                                ..............................
                                                                ..............................
                ______________________________                  ..............................
```
```
(1) Dashboard | (2) Dashboard + Graphs | (3) Suspension | (4) Raw | (Q) Quit | (R) Record/Stop | (L) Load

Front Left      Front Right     Back Left       Back Right
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
        |||              .               .               .
         .               .               .               .
         .              |||             |||             |||
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
         .               .               .               .
```

## How to use
```python main.py```

```
usage: wrc_telemetry [-h] [-c CONFIG] [-i IP] [-p PORT] [-g]

Read UDP telemetry for EA Sports WRC

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        custom1 or custom2 or customX. default custom1
  -i IP, --ip IP        override the used ip. default 127.0.0.1
  -p PORT, --port PORT  override the used port. default 20777
  -g, --isgitbash       uses clear to clear screen to avoid flicker
```

The program should receive packets the moment you start a stage, just before the countdown begins.<br>
Use the keys listed in the top menu to navigate screens (1,2,3,4,Q,R,L).<br>
In the load menu, navigate with arrow keys and enter to select a replay. Scrub through the replay with the right arrow key<br>
Replays are saved to ```logs/``` once you press ```R``` again. They are named after the given config and the timestamp. Note that currently only replays made with the currently active config can be viewed.


## Precondition - Enable UDP telemetry export from the game
Check out YourUser\Documents\My Games\WRC\telemetry.<br>
Located in that directory is ```config.json```, which lists the different default configs for the telemetry.<br>
The game ships with a few example configs called ```wrc``` and ```wrc_experimental```, and a config called ```custom1```.<br>
The client is currently written for ```custom1_mod```.<br>
Might make it more dynamic in the future.<br><br>

Make sure to set ```bEnabled``` for ```custom1_mod``` to ```true``` (game restart needed).<br>
```
{
				"structure": "custom1_mod",
				"packet": "session_update",
				"ip": "127.0.0.1",
				"port": 20777,
				"frequencyHz": -1,
				"bEnabled": true
},
```

WRC Patch 1.6 Update:<br>
This patch introduced new information for the API, but did not provide a config that contains it.<br>
Therefore, i have modified custom1 and will provide the custom1_mod file in this repository. <br>
Make sure you place this in ```YourUser\Documents\My Games\WRC\telemetry\udp``` and make an entry for it in config.json with bEnabled set to true.<br><br>
For the time being, custom1 will remain the default value, as this will be present for every installation of the game. Launch the client with ```-c custom1_mod``` to get car and stage information.

## Known issues and TODOs
* Replaying recorded telemetry data is not guaranteed to run at the correct speed. Therefore 0-100 measurements will be wrong in replays!
* Accelerometer data provided by the game is not bound to the cars orientation. The provided vaules are relative to the fixed directions on the map. I am not sure if I can fix this on my own with the provided telemetry data. imo codies should fix this.
* Limited to fixed structure configs. use ```custom1_mod``` for now.
* SLIP and LOCKUP indicators are based on the difference between GPS speed and transmission speed with a factor. Therefore both are more likely to be detected at lower speeds. Should compute based on the individually provided contact patch information.
* <s>Car and stage info is not available in the UDP telemetry. Could try to check if stage length works as a unique identifier.</s> They added this to the telemetry, no longer relevant.
* Can only scrub forwards through replays, going back is not supported
* <s>Transmission speed column in Dashboard view shifts when GPS speed exceeds 100 Km/h</s>
* Units only calculated in metric
* Reaction to keyboard inputs is currently bound to package handling and is therefore not very responsive
* Replays only available for the currently running config
* <s>Add option to make the histo graph wider and remove the accelerometer graph as its not really useful with the data the telemetry provides</s>
* Add maximum and average suspension travel speed
* <s>Add average suspension travel amount</s>
* <s>Record and store max and min suspension travel amound as well as max suspension travel speed for each car on tarmac and non tarmac. Once all data is gathered, the tool can make more accurate statements about e.g. bottoming out</s>
* Maybe i want to make a database to track all the times you set across all gamemodes with all cars? unfortunately the game does not export weather info.....