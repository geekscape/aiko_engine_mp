# To Do
# ~~~~~
# - Simplify data structure syntax, e.g remove doubling of parameters
# - Put desired "step pattern" into "configuration/step_controller.py"
# - Put led.dim value into .../step_patterns/*.py
# - Make "on_audrey_message()" more generic or move to .../step_patterns/*.py
# - Implement per step ... step period
# - Implement colour interpolation
# - Implement sensors: ambient light, ultrasonics, etc
# - Implement "layer" as a class with behaviour, e.g patterns
# - Implement 7 segment digit

import aiko.event as event
import aiko.led as led
import aiko.mqtt as mqtt

# Provide colors, leds_per_layer, step_speed, steps

# from applications.step_patterns.cchs_1 import *
from applications.step_patterns.skipping_girl import *

step_index = 0

def handle_leds():
  global step_index

  step = steps[step_index]
  step_index = (step_index + 1) % len(steps)

  for action in step:
  # print("ACTION: " + str(action))
    led_start   = action[0] * leds_per_layer
    led_end     = action[1] * leds_per_layer + leds_per_layer
    color_start = colors[action[2]]
    color_end   = colors[action[3]]

    led.dim = 0.3
    for led_index in range(led_start, led_end):
      led.pixel(color_start, led_index)

  led.np.write()

def on_audrey_message(topic, payload_in):
  global colors

  if payload_in.startswith("(audrey:rope "):
    tokens = [int(token) for token in payload_in[13:-1].split()]
    colors[color_rope] = (tokens[0], tokens[1], tokens[2])
    return True

def initialise():
  event.add_timer_handler(handle_leds, step_speed)
  mqtt.add_message_handler(on_audrey_message, "$me/in")
