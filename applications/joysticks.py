# applications/joysticks.py: version: 2018-05-09 00:00
#
# To Do
# ~~~~~
# - None, yet !

from machine import Pin

import json

import aiko.event as event

pins = []
pin_states = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]

# Pin numbers 32, 33, 34, 35 used for buttons
# Pin number 13 used for Wi-Fi LED !

pin_numbers = [
  14, 25, 26, 27,  # controller 0, left  joystick: left, right, down, up
  23, 19,  5, 18,  # controller 0, right joystick: left, right, down, up
   2, 15, 13, 12,  # controller 1, left  joystick: left, right, down, up
  16, 17,  0,  4   # controller 1, right joystick: left, right, down, up
]

pin_axis_map = [
  0, 0, 1, 1, 2, 2, 3, 3,  # controller 0: left and right joysticks
  4, 4, 5, 5, 6, 6, 7, 7   # controller 1: left and right joysticks
]

pin_delta_map = [
  -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1,
  -0.1, 0.1, -0.1, 0.1, -0.1, 0.1, -0.1, 0.1
]

axis_value = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

axis_controller_map = [ 0, 0, 0, 0, 1, 1, 1, 1 ]

axis_name = [ "LH", "LV", "RH", "RV", "LH", "LV", "RH", "RV" ]

def handle_pin(pin):
  try:
    pin_index = pins.index(pin)
    pin_value = pin.value()

    if pin_value:
      pin_states[pin_index] = 1
      return  # Ignore when pin is high

    if pin_states[pin_index] == 0: return  # Ignore if pin was already low
    pin_states[pin_index] = 0

    axis_index = pin_axis_map[pin_index]
    axis_value[axis_index] += pin_delta_map[pin_index]
    if axis_value[axis_index] >  1.0: axis_value[axis_index] =  1.0
    if axis_value[axis_index] < -1.0: axis_value[axis_index] = -1.0

    output_name = axis_name[axis_index]
    output_value = round(axis_value[axis_index], 3)

    payload = {}
    payload["controller"] = axis_controller_map[axis_index]
    payload["action"] = "move"
    payload["axes"] = [(output_name, output_value)]
    payload_out = json.dumps(payload)

    print(payload_out)
  except ValueError:
    print("ERROR: handle_pin(): Unknown Pin argument received")

counter = 0
led_pin = Pin(22, Pin.OUT)

def blink_led():
  global counter
  counter += 1
  led_pin.value(counter % 2)

def initialise():
  for pin_number in pin_numbers:
    pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
    pin.irq(lambda p:handle_pin(p), trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
    pins.append(pin)

  event.add_event_handler(blink_led, 500)
