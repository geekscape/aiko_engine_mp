# main.py: version: 2020-11-29 16:00
#
# Usage
# ~~~~~
# If the application or Aiko framework prevent developer tools from using
# the microPython REPL for interactive access or file transfer, then the
# "denye_touch_pins" parameter can be used to specify the ESP32 capacitive
# touch pins for emergency access.  On boot or whilst developer tools attempt
# to reset the ESP32, press and hold the specified touch pins and the "main.py"
# script will exit.
#
# To Do
# ~~~~~
# - None, yet !

import configuration.main
configuration.globals = globals()         # used by aiko.mqtt.on_exec_message()
parameter = configuration.main.parameter

from machine import Pin, TouchPad
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

import aiko.event
import aiko.net
import aiko.mqtt

import gc
def gc_event():
  gc.collect()
  print("### GC:", gc.mem_free(), gc.mem_alloc())

if parameter("gc_enabled"):                                   # GC: 94736 16432
  aiko.event.add_timer_handler(gc_event, 60000)

import aiko.led                                               # GC: 95264 15904
aiko.led.initialise()

if parameter("oled_enabled"):                                 # GC: 91152 20016
  import aiko.oled
  aiko.oled.initialise()

aiko.net.initialise()                                         # GC: 82752 28416

if parameter("application"):                                  # GC: 82416 28752
  application_name = parameter("application")
  application = __import__(application_name)
  application.initialise()

aiko.event.loop_thread()                                      # GC: 81888 29280
