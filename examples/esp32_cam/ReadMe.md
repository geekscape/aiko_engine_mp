# ESP32-CAM server and desktop/laptop client (viewer)

## ESP32-CAM microPython installation

### Version

* MicroPython v1.20.0-206-g33b403dfb-kaki5 on 2023-07-11; ESP32 CAMERA w/SSL (KAKI5) with ESP32

### Installation

* Download and flash correct ESP32-CAM microPython version (needs specific camera support)
* Edit `server.py` and set your WiFi credentials at line 44.
* Edit `server.py` and set your camera type to "9" at line 84 to select "640x480" resolution. Other resolutions are also available.
* Copy `boot.py`,`main.py` and `server.py` into microPython flash file-system top-level
* Reboot ESP32-CAM

## Desktop/laptop installation

* Tested on Python 3.12.13 (a fair range of Python3 major versions should work)
* `pip install click cv2`  # OpenCV is used for video read and display

## ESP32-CAM console: `streaming_client.py`

Look for ...

* Camera ready ?  True
  * If "False" returned, then power-cycle the ESP32-CAM
* SSID: geekscape_n 
* Wi-Fi connected: 192.168.0.105          <-- required for streaming client connection
  * Camera white LED will briefly flash once ... as a "ready" indicator
* Request from: ('192.168.0.254', 57024)  <-- desktop/laptop streaming client connected

```
s0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:4432
load:0x40078000,len:14148
ho 0 tail 12 room 4
load:0x40080400,len:3332
entry 0x40080618
#### import server
#### server.initialize()
Camera ready ?  True
#### Wi-Fi scan()
SSID: geekscape_n
Wi-Fi not ready. Wait...
E (9933) wifi:Association refused temporarily, comeback time 1024 mSec
Wi-Fi connected: 192.168.0.105
#### server.connect()
E (19113) camera: Value error for PIXFORMAT. 1 to 9 only
Request from: ('192.168.0.254', 57024)
Frame: 73 ms, mem: 2199456
Frame: 37 ms, mem: 2199456
Frame: 34 ms, mem: 2195568
Frame: 53 ms, mem: 2199456
Frame: 37 ms, mem: 2195568
Frame: 33 ms, mem: 2199456
```

## Desktop/laptop console: `streaming_client_0.py`

* Very minimal video read / display client
* ESP32-CAM IP address is hard-coded ... look at ESP32-CAM console log for server IP addresss
* Currently, no console output
* If video window shows "three copies", stop and restart the streaming client

```
$ python3 streaming_client_0.py 
```

## Desktop/laptop console: `streaming_client_1.py`

* Command line arguments for streaming server URL, statistics, etc
  * Use `--help` option for usage details
* Displays frame capture time (milliseconds) and frame-rate (FPS)
* If video window shows "three copies", stop and restart the streaming client

```
$ python3 streaming_client_1.py --help
```

```
$ python3 streaming_client_1.py 
Connecting: http://192.168.0.105/username/password
frames=      10  avg_dt(10/10)=  94.20 ms  avg_fps= 10.62
frames=      20  avg_dt(10/10)=  81.51 ms  avg_fps= 12.27
frames=      30  avg_dt(10/10)=  84.36 ms  avg_fps= 11.85
frames=      40  avg_dt(10/10)=  87.77 ms  avg_fps= 11.39
```

```
$ python3 streaming_client_1.py --url http://192.168.0.105/username/password --avg-n 10 --wait-ms 1
```
