# lib/aiko/common.py: version: 2020-12-27 14:00 v05
#
# To Do
# ~~~~~
# - Improve set_handler() mechanism to not require individual handler shims
# - Refactor touch_pins_check() into "lib/aiko/button.py"

from machine import Pin, TouchPad, unique_id
import os

AIKO_VERSION = "v04"

handlers = {}
# mutex = False
touch_okay = True

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
        if TouchPad(Pin(touch_pin)).read() < 200:  # TODO: Fix literal "200"
          touched_pins += 1
    except Exception:
      touch_okay = False

    if touched_pins == len(touch_pins): return True
  return False

def serial_id():
  id = unique_id()  # 6 bytes
  id = "".join(hex(digit)[-2:] for digit in id)
  return id  # 12 hexadecimal digits
