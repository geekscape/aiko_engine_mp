# applications/nodebots.py: version: 2018-05-16 00:00
#
# To Do
# ~~~~~
# - None, yet !

from machine import Pin

# import configuration.nodebots

import aiko.event as event
import aiko.mqtt as mqtt

led_pin = Pin(22, Pin.OUT)

MODE_INPUT = 0
MODE_OUTPUT = 1
MODE_ANALOG = 2
MODE_PWM = 3
MODE_SERVO = 4

pins = {}

def on_nodebots_message(topic, payload_in):
  print("on_nodebots_message(): " + payload_in)
  if payload_in.startswith("(nb:pin_mode "):
    tokens = [int(token) for token in payload_in[13:-1].split()]
    pin = int(tokens[0])
    mode = int(tokens[1])
    if mode >=0 and mode <=1:
      pins[pin] = mode
    return True

  if payload_in.startswith("(nb:digital_write "):
    tokens = [int(token) for token in payload_in[18:-1].split()]
    pin = int(tokens[0])
    value = int(tokens[1])
    led_pin.value(value)
    return True

def initialise():
  mqtt.add_message_handler(on_nodebots_message, "$me/in")
