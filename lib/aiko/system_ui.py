# lib/aiko/system_ui.py: version: 2021-01-22 18:00 v05
#
# To Do
# ~~~~~
# - Consider creating "process.py", which encapsulates process data structures

from threading import Thread

import aiko.oled as oled

import configuration.system_ui

system_ui_active = False

def system_features_handler(pin_numbers):
  global system_ui_active
  system_ui_active = not system_ui_active

  if system_ui_active:
    oled.set_system_title(save=True)
    oled.oleds_clear()
    oled.oleds_enable(False)
  else:
    oled.oleds_enable(True)
    oled.set_system_title(restore=True)
    oled.oleds_clear()

def initialise(settings=configuration.system_ui.settings):
  system_ui_pins = configuration.main.parameter("system_ui_pins", settings)
  if system_ui_pins:
    import aiko.button
    aiko.button.initialise()
    aiko.button.add_multibutton_handler(system_features_handler, system_ui_pins)

def console_log_feature():
  pass

def firmware_upgrade_feature():
  pass

features = [
  ("Console log", console_log_feature),
  ("Firmware upgrade", firmware_upgrade_feature)
]
