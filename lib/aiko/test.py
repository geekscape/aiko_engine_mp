# lib/aiko/test.py: version: 2020-12-07 20:00
#
# Usage
# ~~~~~
# import aiko.test as test
# test.echo("Go away, I'm busy !")
# test.set_pin_list([19, 22])   # Set list of pin numbers
# test.get_pin_list()           # Get list of pin numbers
# test.set_pins_mode(0)         # Mode: Output
# test.set_pins_mode(1)         # Mode: Input pull-down
# test.set_pins_mode(2)         # Mode: Input pull-up
# test.pins                     # Check that pins have been initialised
# test.set_pins_value(0)        # Set all pins low
# test.set_pins_value(1)        # Set all pins high
# test.set_pin_value(index, 0)  # Set single pin[index] low
# test.set_pin_value(index, 1)  # Set single pin[index] high
# test.get_pins_value()         # Check all pin input values
#
# To Do
# ~~~~~
# - Command to log to the OLED screen
# - Set touch pin list
# - Get touch pin values

import machine

pin_list = [
  19,  # SAO#1
  22,  #  " "
  32,  # SAO#2
  33,  #  " "
  18,  # SAO#3
  23,  #  " "
  25,  # SAO#4
  22,  #  " "
#  0,  # Left side header
   2,  #  "    "    "  "
  13,  #  "    "    "  "
# 34,  # Right side header (input only)
# 35   #  "     "    "  "  (input only)
]

# 15  # top left touch button (T3)
# 12  # bottom left touch button (T5)
# 27  # top right touch button (T7)
# 14  # bottom right touch button (T6)

# 16  # left OLED button
# 17  # right OLED button

pin_mode = [
  (machine.Pin.OUT, None),
  (machine.Pin.IN, machine.Pin.PULL_DOWN),
  (machine.Pin.IN, machine.Pin.PULL_UP)
]

pins = None

def echo(message):
  print(message)

def get_pin_list():
  print("(pass get_pin_list: " + str(pin_list) + ")")

def get_pins_value():
  values = []
  for pin in pins:
    values.append(pin.value())
  print("(pass get_pins_value: " + str(values) + ")")

def set_pin_list(_pin_list):
  global pin_list
  pin_list = _pin_list
  print("(pass set_pin_list)")

def set_pins_mode(mode):
  global pin_list, pins
  pins = []

  direction = pin_mode[mode][0]
  pull = pin_mode[mode][1]

  for pin_number in pin_list:
    if pull:
      pin = machine.Pin(pin_number, direction, pull)  # Input
    else:
      try:
        pin = machine.Pin(pin_number, direction)  # Output
      except ValueError:
        print("(fail set_pins_mode input only: " + str(pin_number) + ")")
        return
    pins.append(pin)

  print("(pass set_pins_mode)")

def set_pin_value(index, value):
  pins[index].value(value)
  print("(pass set_pin_value)")

def set_pins_value(value):
  for pin in pins:
    pin.value(value)
  print("(pass set_pins_value)")

print("(pass aiko.test)")
