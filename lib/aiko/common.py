# lib/aiko/common.py: version: 2020-12-27 14:00 v05
#
# To Do
# ~~~~~
# - Improve set_handler() mechanism to not require individual handler shims
# - Refactor touch_pins_check() into "lib/aiko/button.py"

from machine import Pin, TouchPad, unique_id
import os

AIKO_VERSION = "v05"
ANNUNCIATOR_LOG  = 1
ANNUNCIATOR_MQTT = 2
ANNUNCIATOR_WIFI = 3

annunicator_log_symbol = "L"

handlers = {}
# mutex = False
touch_okay = True

def convert_time(timer):
  seconds = timer % 60
  minutes = (timer - seconds) // 60 % 60
  hours = (timer - minutes * 60 - seconds) // 3600
  return hours, minutes, seconds

def hostname():
  return os.uname()[0] + "_" + serial_id()

# def lock(state):
#   global mutex
#   if state:
#     yield
#     while True:
#       if not mutex:
#         mutex = True
#         return True
#       yield False
#   else:
#     mutex = False

def log(message):
  if "log" in handlers:
    handlers["log"](message)

def map_value(input, in_min, in_max, out_min, out_max):
  output = (input-in_min) / (in_max-in_min) * (out_max-out_min) + out_min
  output = max(output, out_min)
  output = min(output, out_max)
  return output

def set_handler(name, handler):
  handlers[name] = handler

def touch_pins_check(touch_pins):
  global touch_okay

  if touch_pins and touch_okay:
    touched_pins = 0
    try:
      for touch_pin in touch_pins:
        try:
          TouchPad(Pin(touch_pin)).read()
        except Exception:
          print("### Main: Touch calibration issue on GPIO: " + str(touch_pin))
        if TouchPad(Pin(touch_pin)).read() < 150:  # TODO: Fix literal "150"
          touched_pins += 1
    except Exception:
      touch_okay = False

    if touched_pins == len(touch_pins): return True
  return False

def serial_id():
  id = unique_id()  # 6 bytes
  id = "".join(hex(digit)[-2:] for digit in id)
  return id  # 12 hexadecimal digits
