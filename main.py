# main.py: version: 2020-11-29 16:00
#
# Usage
# ~~~~~
# If the application or Aiko framework prevent developer tools from using
# the microPython REPL for interactive access or file transfer, then the
# "denye_touch_pins" parameter can be used to specify ESP32 capacitive
# touch pins for emergency access.  On boot or whilst developer tools attempt
# to reset the ESP32, press the specified touch pins and the "main.py" script
# will exit.
#
# To Do
# ~~~~~
# - None, yet !

import aiko.event as event
from machine import Pin, TouchPad

import configuration.main
configuration.globals = globals()         # used by aiko.mqtt.on_exec_message()
parameter = configuration.main.parameter

touch_pins = parameter("denye_touch_pins")
if touch_pins:
  touched_pins = 0
  for touch_pin in touch_pins:
    try:
      TouchPad(Pin(touch_pin)).read()
    except Exception:
      print("### MAIN: Touch calibration issue on GPIO: " + str(touch_pin))
    if TouchPad(Pin(touch_pin)).read() < 200:
      touched_pins += 1
  if touched_pins == len(touch_pins):
    raise Exception("Exit to repl")

import gc
def gc_event():
  gc.collect()
  print("### GC:", gc.mem_free(), gc.mem_alloc())

if parameter("gc_enabled"):                                  # GC: 105984  5184
  event.add_timer_handler(gc_event, 60000)

import aiko.led as led                                       # GC:  94784 16384
led.initialise()

if parameter("oled_enabled"):                                # GC:  86528 24640
  import aiko.oled as oled
  oled.initialise()

import aiko.net as net                                       # GC:  85424 25744
net.initialise()

if parameter("application"):                                 # GC:  85056 26112
  application_name = parameter("application")
  application = __import__(application_name)
  application.initialise()

event.loop_thread()                                          # GC:  85104 26064
