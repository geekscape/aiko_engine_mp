# lib/aiko/system.py: version: 2021-01-22 18:00 v05
#
# To Do
# ~~~~~
# - None, yet !

import configuration.system

def system_features_handler(pin_numbers):
  print("System special features")

def initialise(settings=configuration.system.settings):
  system_pins = configuration.main.parameter("system_pins", settings)
  if system_pins:
    import aiko.button
    aiko.button.initialise()
    aiko.button.add_multibutton_handler(system_features_handler, system_pins)
