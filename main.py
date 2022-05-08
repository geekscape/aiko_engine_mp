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

# load_plugins(): Load all files from the 'plugins/' folder (instanced into $plugins["plugin_name"])
def load_plugins():
  import os
  plugins = dict()
  print("[Plugin] Searching for plugins...")
  for plugin_file in os.listdir('plugins'):                      # Find all files in the 'plugin' folder
    plugin_name = plugin_file[:-3]                                # Strip .py extension
    print("[Plugin] Loading Plugin '{}'\t(from path: 'plugins/{}')".format(plugin_name, plugin_file))
    try:
        plugins[plugin_name] = __import__("plugins/{}".format(plugin_name), globals(), locals(  ), [plugin_name])
    except ImportError as plugin_error:
        print("[Plugins] Error loading plugin '{}'\t{}".format(plugin_name, plugin_error), False)
        continue

# Plugin System - enable with plugins_enabled flag
if parameter("plugins_enabled"):
  load_plugins()

aiko.event.loop_thread()
