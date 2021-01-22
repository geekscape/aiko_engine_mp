# lib/aiko/system_ui.py: version: 2021-01-22 18:00 v05
#
# To Do
# ~~~~~
# - When required, increase maximum displayable menu items beyond 5
# - Consider creating "process.py", which encapsulates process data structures

import aiko.button
from aiko.common import map_value
import aiko.oled as oled

import configuration.system_ui

system_ui_active = False

menu_item_highlighted = 0

def system_features_handler(pin_numbers):
  global system_ui_active
  system_ui_active = not system_ui_active

  if system_ui_active:
    aiko.button.add_slider_handler(slider_handler, 12, 15)
    oled.set_system_title(save=True)
    oled.oleds_clear(write=False)
    menu_show()
    menu_item_highlight(0)
    oled.oleds_enable(False)
  else:
    aiko.button.remove_handler(slider_handler)
    oled.oleds_enable(True)
    oled.set_system_title(restore=True)
    oled.oleds_clear()

def initialise(settings=configuration.system_ui.settings):
  system_ui_pins = configuration.main.parameter("system_ui_pins", settings)
  if system_ui_pins:
    aiko.button.initialise()
    aiko.button.add_multibutton_handler(system_features_handler, system_ui_pins)

def slider_handler(number, state, value):
  if value:
    menu_item = menu_items - int(map_value(value, 0, 100, 0, menu_items-1)) - 1
    menu_item_highlight(menu_item)

def menu_item_highlight(menu_item):
  global menu_item_highlighted
  oled.oleds_system_use(True)
  menu_item_write(menu_item_highlighted)
  menu_item_highlighted = menu_item
  menu_item_write(menu_item_highlighted, highlighted=True)
  oled.oleds_show()
  oled.oleds_system_use(False)

def menu_item_write(menu_item, highlighted=False):
  feature_name = features[menu_item][FEATURE_NAME]
  color = oled.FG if highlighted else oled.BG
  oled.oleds[0].fill_rect(0, menu_item * 10 + 10, 128, 10, color)
  color = oled.BG if highlighted else oled.FG
  oled.oleds_text(feature_name, 0, menu_item * 10 + 11, color)

def menu_show():
  for menu_item in range(len(features)):
    menu_item_write(menu_item)

def console_log_feature():
  pass

def firmware_upgrade_feature():
  pass

features = [
  ("Console log", console_log_feature),
  ("Firmware upgrade", firmware_upgrade_feature)
]

FEATURE_NAME = 0

menu_items = len(features)
