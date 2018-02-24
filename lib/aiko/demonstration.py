# lib/aiko/demonstration.py: version: 2018-02-11 00:00
#
# Usage
# ~~~~~
# import aiko.demonstration as demo
# demo.set_handler(demo.pattern_1)
# event.add_event_handler(demo.handler, 100)
#
# demo.set_handler(None)
#
# To Do
# ~~~~~
# - demonstration.handler(): implement "rate" or "time_period"
# - Implement "configuration/demonstration.py"
# - Allow input to control pattern(s), e.g sensors and/or MQTT messages

from time import ticks_ms
import urandom

import aiko.led as led

demonstration = None

def handler():
  if demonstration:
#   start = ticks_ms()
    demonstration()
#   print(">> " + str(start / 1000)  + ": " + str(ticks_ms() - start))

def set_handler(demonstration_handler):
  global demonstration
  demonstration = demonstration_handler

# pattern_1(): Random pixels
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
p1_setup = True
p1_pixel_batch = 50
p1_pixel_color = "white"

def pattern_1():  # 36 milliseconds + p1_pixel_batch * 1 millisecond
  global p1_setup, p1_pixel_color
  if p1_setup:
    p1_setup = False
    led.dim = 0.02

  for count in range(p1_pixel_batch): led.random_pixel()
  led.pixel(led.colors[p1_pixel_color], 0, True)
  p1_pixel_color = "black" if p1_pixel_color == "white" else "white"

# pattern_2(): Snake
# ~~~~~~~~~~~~~~~~~~
p2_color = led.black
p2_delta = led.black
p2_direction = 0
p2_length = 0
p2_x = int(led.length_x / 2)
p2_y = int(led.length_x / 2)

def pattern_2():
  global p2_color, p2_delta, p2_direction, p2_length, p2_x, p2_y

  if p2_length == 0:
    p2_length = urandom.randint(int(led.length_x / 4), int(led.length_x * 3/4))

    while True:                                        # avoid 180 degree turns
      direction = urandom.randint(0, 3)
      if direction != (p2_direction + 2) % 4:
        p2_direction = direction
        break

    color = led.random_color()                         # smooth transition
    delta_red   = (color[0] - p2_color[0]) / p2_length
    delta_green = (color[1] - p2_color[1]) / p2_length
    delta_blue  = (color[2] - p2_color[2]) / p2_length
    p2_delta = (delta_red, delta_green, delta_blue)

  if p2_direction == 0: p2_x = (p2_x + 1) % led.length_x
  if p2_direction == 1: p2_y = (p2_y + 1) % led.length_x
  if p2_direction == 2: p2_x = (p2_x - 1) % led.length_x
  if p2_direction == 3: p2_y = (p2_y - 1) % led.length_x

  red   = p2_color[0] + p2_delta[0]
  green = p2_color[1] + p2_delta[1]
  blue  = p2_color[2] + p2_delta[2]
  p2_color = (red, green, blue)

  led.pixel_xy(p2_color, p2_x, p2_y, write=True)
  p2_length -= 1
