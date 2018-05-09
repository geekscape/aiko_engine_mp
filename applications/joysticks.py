# applications/joysticks.py: version: 2018-05-09 00:00
#
# To Do
# ~~~~~
# - None, yet !

from machine import Pin

import json

import aiko.event as event

pins = []
pins_active = []

# Pin number 13 used for Wi-Fi LED and one of the joysticks !
# Pin numbers 32, 33, 34, 35 will be used for buttons

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

axis_controller_map = [ 0, 0, 0, 0, 1, 1, 1, 1 ]

axis_name = [ "LH", "LV", "RH", "RV", "LH", "LV", "RH", "RV" ]

axis_value = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

def handle_pin_change(pin):
  try:
    pin_index = pins.index(pin)          # Will raise ValueError on unknown pin

    if not pin.value():
      if not pin in pins_active: pins_active.append(pin)
    else:
      if pin in pins_active:
        pins_active.remove(pin)
        axis_value[pin_axis_map[pin_index]] = 0.0

  except ValueError:
    print("ERROR: handle_pin_change(): Unknown Pin argument received")

def handle_pins_active():
  for pin in pins_active:
    pin_index = pins.index(pin)
    axis_index = pin_axis_map[pin_index]
    axis_value[axis_index] += pin_delta_map[pin_index]
    if axis_value[axis_index] >  1.0: axis_value[axis_index] =  1.0
    if axis_value[axis_index] < -1.0: axis_value[axis_index] = -1.0

    output_value = round(axis_value[axis_index], 3)

    payload = {}
    payload["controller"] = axis_controller_map[axis_index]
    payload["action"] = "move"
    payload["axes"] = [(axis_name[axis_index], output_value)]
    payload_out = json.dumps(payload)
    print(payload_out)

counter = 0
led_pin = Pin(22, Pin.OUT)

def handle_blink_led():
  global counter
  counter += 1
  led_pin.value(counter % 2)

def initialise():
  for pin_number in pin_numbers:
    pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
    pin.irq(lambda p:handle_pin_change(p),
              trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
    pins.append(pin)

  event.add_event_handler(handle_pins_active, 50)  # 20 Hz
  event.add_event_handler(handle_blink_led, 500)
