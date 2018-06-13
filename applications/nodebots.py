# applications/nodebots.py: version: 2018-06-13 00:00
#
# Johnny-Five NodeBots adaptor: https://github.com/ajfisher/aiko-io
#
# Resources
# ~~~~~~~~~
# - https://github.com/rwaldron/io-plugins#pinmodepin-mode
#
# To Do
# ~~~~~
# - Input pin poll, similar to joystick hardware interrupt trigger
# - Default poll sample rate, which can be changed from the host
#
# - Consider how to send back errors to host, e.g pin not capable
#   - Pin 34 and 35 have no internal pull-up
#
# Pin 22: Blue LED (Lolin32-Lite)
# Pins 12, 14, 27, 26, 25, 33, 32, 35, 34

from machine import Pin

led_pin = Pin(12, Pin.OUT)

# import configuration.nodebots

import aiko.event as event
import aiko.mqtt as mqtt

MODE_INPUT  = 0
MODE_OUTPUT = 1
MODE_ANALOG = 2
MODE_PWM    = 3
MODE_SERVO  = 4
MODE_DAC    = 5

pins_info = {}

def on_nodebots_message(topic, payload_in):
  print("on_nodebots_message(): " + payload_in)

  if payload_in.startswith("(nb:pin_mode "):
    tokens = [int(token) for token in payload_in[13:-1].split()]
    pin_number = tokens[0]
    pin_mode = tokens[1]
    pin = None

    if pin_mode == MODE_INPUT:
      pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
#     pin.irq(lambda p:handle_pin_change(p),
#       trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    elif pin_mode == MODE_OUTPUT:
      pin = Pin(pin_number, Pin.OUT)

    if pin:
      pins_info[pin_number] = { "mode": pin_mode, "pin": pin }
    return True

  if payload_in.startswith("(nb:digital_write "):
    tokens = [int(token) for token in payload_in[18:-1].split()]
    pin_number = tokens[0]
    value = tokens[1]

    if pin_number in pins_info:
      pin_info = pins_info[pin_number]
      if pin_info["mode"] == MODE_OUTPUT:
        pin_info["pin"].value(value)
    return True

def initialise():
  mqtt.add_message_handler(on_nodebots_message, "$me/in")
