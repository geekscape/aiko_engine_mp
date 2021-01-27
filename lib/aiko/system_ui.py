# lib/aiko/system_ui.py: version: 2021-01-22 18:00 v05
#
# To Do
# ~~~~~
# - When required, increase maximum displayable menu items beyond 5
# - Create "processes", which encapsulate process data structures
# - UI in "oled.py" can be (1) just for process or (2) share with console log

import aiko.button
from aiko.common import map_value
import aiko.oled as oled
import aiko.upgrade

import configuration.system_ui

system_ui_active = False

menu_item_selected = 0

def system_features_handler(pin_numbers):
  global system_ui_active
  system_ui_active = not system_ui_active

  if system_ui_active:
    system_features_menu()
    aiko.button.add_touch_handler(button_handler, [14, 27])
    oled.oleds_enable(False)
  else:
    aiko.button.remove_handler(button_handler)
    aiko.button.remove_handler(slider_handler)
    oled.oleds_enable(True)
    oled.set_system_title(restore=True)
    oled.oleds_clear()

def initialise(settings=configuration.system_ui.settings):
  system_ui_pins = configuration.main.parameter("system_ui_pins", settings)
  if system_ui_pins:
    aiko.button.initialise()
    aiko.button.add_multibutton_handler(system_features_handler, system_ui_pins)

def button_handler(number, state):
  global menu_item_selected
  if state:
    if number == 14:
# TODO: button and multibutton handlers are still active !
      aiko.button.remove_handler(slider_handler)
      features[menu_item_selected][HANDLER]()
    if number == 27:
      system_features_menu()

def slider_handler(number, state, value):
  if value:
    menu_item = menu_items - int(map_value(value, 0, 100, 0, menu_items-1)) - 1
    menu_item_select(menu_item)

def system_features_menu():
  oled.oleds_system_use(True)
  aiko.button.add_slider_handler(slider_handler, 12, 15)
  oled.set_system_title(save=True)
  oled.oleds_clear(write=False)
  menu_show()
  menu_item_select(0)
  oled.oleds_system_use(False)

def menu_item_select(menu_item):
  global menu_item_selected
  oled.oleds_system_use(True)
  menu_item_write(menu_item_selected)
  menu_item_selected = menu_item
  menu_item_write(menu_item_selected, selected=True)
  oled.oleds_show()
  oled.oleds_system_use(False)

def menu_item_write(menu_item, selected=False):
  feature_name = features[menu_item][NAME]
  color = oled.FG if selected else oled.BG
  oled.oleds[0].fill_rect(0, menu_item * 10 + 10, 128, 10, color)
  color = oled.BG if selected else oled.FG
  oled.oleds_text(feature_name, 0, menu_item * 10 + 11, color)

def menu_show():
  for menu_item in range(len(features)):
    menu_item_write(menu_item)
  version = aiko.upgrade.get_version()
  if version:
    oled.oleds[1].text("Firmware upgrade", 0, 11, oled.FG)
    oled.oleds[1].text("Version: " + version, 0, 21, oled.FG)

def console_log_feature():
  oled.oleds_system_use(True)
  oled.oleds_show_log()
  oled.oleds_system_use(False)

hugs_message = [ "", "hey Leon,", "Let's figure", "something out ?", "... andyg :)" ]

def hugs_feature():
  oled.oleds_system_use(True)
  oled.oleds_show_log(hugs_message)
  oled.oleds_system_use(False)

features = [
  ("Console log", console_log_feature),
  ("Firmware upgrade", aiko.upgrade.upgrade_handler),
  ("Hugs ???", hugs_feature),
]

NAME = 0
HANDLER = 1

menu_items = len(features)
