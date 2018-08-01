# applications/nodebots.py: version: 2018-06-13 00:00
#
# Johnny-Five NodeBots adaptor: https://github.com/ajfisher/aiko-io
#
# Messages
# ~~~~~~~~
# - (nb:pin_mode PIN_NUMBER PIN_MODE)
# - (nb:digital_read PIN_NUMBER)
# - (nb:digital_write PIN_NUMBER PIN_VALUE)
#
# Resources
# ~~~~~~~~~
# - https://github.com/rwaldron/io-plugins#pinmodepin-mode
#
# To Do
# ~~~~~
# - Input pin poll, similar to joystick hardware interrupt trigger
# - Default poll sample rate, which can be changed from the host
#   - 50 Hz to 200 Hz
#
# - Consider how to send back errors to host, e.g pin not capable
#   - Pin 34 and 35 have no internal pull-up
#
# Pin 22: Blue LED (Lolin32-Lite)
# Pins 12, 14, 27, 26, 25, 33, 32, 35, 34

import machine
from machine import Pin

# led_pin = Pin(12, Pin.OUT)

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
pins_input = []

def handle_pin_change(pin):              ### hardware pin interrupt handler ###
  pass

def handle_pins_input():                 ### software timer event handler ###
  irq_state = machine.disable_irq()
  local_pins_input = [pin for pin in pins_input]
  machine.enable_irq(irq_state)

  for pin_number in local_pins_input:
    value = pins_info[pin_number]["pin"].value()
    mqtt.client.publish(mqtt.topic_path + "/out",
      "(nb:pin_value " + str(pin_number) + " " + str(value) + ")")

def on_nodebots_message(topic, payload_in):
  print("on_nodebots_message(): " + payload_in)

  if payload_in.startswith("(nb:pin_mode "):
    tokens = [int(token) for token in payload_in[13:-1].split()]
    pin_number = tokens[0]
    pin_mode = tokens[1]
    pin = None

    if pin_number in pins_input:
      pins_input.remove(pin_number)

    if pin_mode == MODE_INPUT:
      pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
      pins_input.append(pin_number)
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
  event.add_event_handler(handle_pins_input, 50)  # 20 Hz
  mqtt.add_message_handler(on_nodebots_message, "$me/in")
