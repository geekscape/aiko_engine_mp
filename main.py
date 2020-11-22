# main.py: version: 2020-11-22 19:00
#
# To Do
# ~~~~~
# - None, yet !

import aiko.event as event

import configuration.main
configuration.globals = globals()         # used by aiko.mqtt.on_exec_message()
parameter = configuration.main.parameter

import gc
def gc_event():
  gc.collect()
  print("  ###### GC:", gc.mem_free(), gc.mem_alloc())

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
