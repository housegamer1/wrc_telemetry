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

## Precondition - Enable UDP telemetry export from the game
Check out YourUser\Documents\My Games\WRC\telemetry.<br>
Located in that directory is ```config.json```, which lists the different default configs for the telemetry.<br>
The game ships with a few example configs called ```wrc``` and ```wrc_experimental```, and a config called ```custom1```.<br>
This is the config the client is currently written for (essentially it is the same as ```wrc```).<br>
Might make it more dynamic in the future.<br><br>

Make sure to set ```bEnabled``` for ```custom1``` to true (game restart needed).<br>
```
{
				"structure": "custom1",
				"packet": "session_update",
				"ip": "127.0.0.1",
				"port": 20777,
				"frequencyHz": -1,
				"bEnabled": true
},
```


## Known issues and TODOs
* Replaying recorded telemetry data is not guaranteed to run at the correct speed
* Accelerometer data provided by the game is not bound to the cars orientation. The provided vaules are relative to the fixed directions on the map. I am not sure if I can fix this on my own with the provided telemetry data. imo codies should fix this.
* Limited to fixed structure configs. use ```custom1```
* SLIP and LOCKUP indicators are based on the difference between GPS speed and transmission speed with a factor. Therefore both are more likely to be detected at lower speeds. Should compute based on the individually provided contact patch information.
* Car and stage info is not available in the UDP telemetry. Could try to check if stage length works as a unique identifier.
* Can only scrub forwards through replays, going back is not supported
* Transmission speed column in Dashboard view shifts when GPS speed exceeds 100 Km/h
* Units only calculated in metric
* Reaction to keyboard inputs is currently bound to package handling and is therefore not very responsive