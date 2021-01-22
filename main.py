# main.py: version: 2021-01-22 18:00 v05
#
# Usage
# ~~~~~
# If the application or Aiko framework prevent developer tools from using
# the microPython REPL for interactive access or file transfer, then the
# "denye_pins" parameter can be used to specify the ESP32 capacitive
# touch pins for emergency access.  On boot or whilst developer tools attempt
# to reset the ESP32, press and hold the specified touch pins and the "main.py"
# script will exit.
#
# To Do
# ~~~~~
# - None, yet.

import configuration.main
configuration.globals = globals()  # used by aiko.mqtt.on_exec_message()
parameter = configuration.main.parameter

denye_pins = parameter("denye_pins")
import aiko.common as common
if common.touch_pins_check(denye_pins):
  raise Exception("Exit to repl")

import aiko.event
import aiko.net
import aiko.mqtt
import aiko.system_ui
aiko.system_ui.initialise()

import aiko.led
aiko.led.initialise()

if parameter("oled_enabled"):
  import aiko.oled
  aiko.oled.initialise()

import aiko.upgrade
aiko.upgrade.initialise()

aiko.net.initialise()

if parameter("application"):
  application_name = parameter("application")
  application = __import__(application_name)
  application.initialise()

aiko.event.loop_thread()
