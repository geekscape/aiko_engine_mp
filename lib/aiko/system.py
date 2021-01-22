# lib/aiko/system.py: version: 2021-01-22 18:00 v05
#
# To Do
# ~~~~~
# - None, yet !

import aiko.oled as oled

import configuration.system

system_active = False

def system_features_handler(pin_numbers):
  global system_active
  system_active = not system_active

  if system_active:
    oled.set_system_title(save=True)
    oled.oleds_clear()
    oled.oleds_enable(False)
  else:
    oled.oleds_enable(True)
    oled.set_system_title(restore=True)
    oled.oleds_clear()

def initialise(settings=configuration.system.settings):
  system_pins = configuration.main.parameter("system_pins", settings)
  if system_pins:
    import aiko.button
    aiko.button.initialise()
    aiko.button.add_multibutton_handler(system_features_handler, system_pins)

def console_log_feature():
  pass

def firmware_upgrade_feature():
  pass

features = [
  ("Console log", console_log_feature),
  ("Firmware upgrade", firmware_upgrade_feature)
]
