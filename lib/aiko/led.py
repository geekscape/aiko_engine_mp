# lib/aiko/led.py: version: 2020-12-27 14:00 v05
#
# Usage
# ~~~~~
# from aiko import led
# led.initialise()
# led.pixel(aiko.led.red, 0, True)
#
# MQTT commands
# ~~~~~~~~~~~~~
# Topic: /in   (led:clear)
#              (led:dim 0.02)
#              (led:fill  R G B)
#              (led:line  R G B X0 Y0 X1 Y1)
#              (led:pixel R G B X)
#              (led:write)
#              (led:write R G B ...)
#
# Topic: /in   (led:traits)
#        /out  (led:traits rgb LED_COUNT)
#
# To Do
# ~~~~~
# - Only register MQTT on_led_message() if MQTT is enabled
#
# Notes
# ~~~~~
# - https://github.com/micropython/micropython-esp32/blob/esp32/ports/esp32/espneopixel.c
# - https://github.com/micropython/micropython-esp32/issues/159
# - https://forum.micropython.org/viewtopic.php?f=18&t=3697&p=21460&hilit=neopixel#p21460
# - https://forum.micropython.org/viewtopic.php?f=18&t=3769&p=21741&hilit=neopixel#p21741

from machine  import Pin
from neopixel import NeoPixel

import configuration.led
import configuration.main

import urandom
apa106   = False
# this is overrriden by value read from settings at init time
dim      = 0.1  # 100% = 1.0
full     = 255
length   = None
length_x = None
locked   = 0
np       = None
zigzag   = False

colors = {
  "black":  (   0,    0,    0),
  "red":    (full,    0,    0),
  "green":  (   0, full,    0),
  "blue":   (   0,    0, full),
  "purple": (full,    0, full),
  "yellow": (full, full,    0),
  "white":  (full, full, full)
}

black = colors["black"]
red = colors["red"]
green = colors["green"]
blue = colors["blue"]
yellow = colors["yellow"]

def apply_dim(color, dimmer=None):
  if dimmer == None: dimmer = dim
  red   = int(color[0] * dimmer)
  green = int(color[1] * dimmer)
  blue  = int(color[2] * dimmer)
  return (red, green, blue)
# TODO: Now fails when called by exec(), see lib/aiko/mqtt.py
# return tuple([int(element * dimmer) for element in color])

# Allow setting dim from code or MQTT
def set_dim(dimmer):
    global dim
    dim = dimmer

# this is used to turn the neopixels back on to default brightness
def reset_dim():
  parameter = configuration.main.parameter
  set_dim(parameter("dim", configuration.led.settings))

# Take from -0.9 to 0.9 (+-0.1 is more typical) and adjust diming
# value. Make sure it stays within 0 to 1
def change_dim(change):
    global dim
    dim += change
    if dim<0: dim=0
    if dim>1: dim=1

def print_dim():
    print("Dim: ", dim)

def fill(color, write=True):
  np.fill(apply_dim((color[0], color[1], color[2])))
  if write: np.write()

# write is needed if you use fill() or lots of pixel writes
# and then you decide to push the result.
def write():
  np.write()

# Bresenham's line algorithm
def line(color, x0, y0, x1, y1):
  x_delta = abs(x1 - x0);
  y_delta = abs(y1 - y0);
  x_increment = 1 if x0 < x1 else -1
  y_increment = 1 if y0 < y1 else -1
  error = (y_delta if y_delta > x_delta else -x_delta) / 2

  while True:
    pixel_xy(color, x0, y0)
    if y0 == y1 and x0 == x1: break
    error2 = error

    if error2 > -y_delta:
      error -= x_delta
      y0 += y_increment

    if error2 < x_delta:
      error += y_delta
      x0 += x_increment

def linear(dimension):
  if type(dimension) == int: return dimension
  result = 1
  for index in range(len(dimension)): result *= dimension[index]
  return result

def random_color():
  red   = urandom.randint(0, full)
  green = urandom.randint(0, full)
  blue  = urandom.randint(0, full)
  return (red, green, blue)

def random_position():
  return urandom.randint(0, length - 1)

def pixel(color, x=0, write=False, lock=None):
  if lock is None: lock = locked
  if apa106: color = (color[1], color[0], color[2])
  if zigzag and (x // length_x) % 2:
    x = length_x * (x // length_x + 1) - (x - length_x * (x // length_x)) - 1
  if x >= lock and x < length: np[x] = apply_dim(color)
  if write: np.write()

def pixel0(color):
  np[0] = color
  saved_buffer = np.buf
  np.buf = bytearray(3)
  np[0] = color
  np.write()
  np.buf = saved_buffer

def pixel_get(x=0):
  if zigzag and (x // length_x) % 2:
    x = length_x * (x // length_x + 1) - (x - length_x * (x // length_x)) - 1
  return np[x]

def random_pixel(write=False):
  pixel(random_color(), random_position(), write)

def pixel_xy(color, x=0, y=0, write=False):
  pixel(color, x + y * length_x, write)

def initialise(settings=configuration.led.settings):
  global apa106, length, length_x, np, zigzag

  parameter = configuration.main.parameter
  apa106 = parameter("apa106", settings)
  zigzag = parameter("zigzag", settings)
  reset_dim()

  length = linear(settings["dimension"])
  length_x = settings["dimension"][0]
  np = NeoPixel(Pin(settings["neopixel_pin"]), length, timing=True)

  import aiko.mqtt
  aiko.mqtt.add_message_handler(on_led_message, "$me/in")

def on_led_message(topic, payload_in):
  if payload_in == "(led:clear)":
    fill(black)
    np.write()
    return True

  if payload_in.startswith("(led:dim "):
    tokens = [float(token) for token in payload_in[9:-1].split()]
    set_dim(tokens[0])
    return True

  # When I send one debug message, this gets printed twice. Why?
  if payload_in == "(led:debug)":
    print_dim()
    print("length: ", length)

  if payload_in.startswith("(led:fill "):
    tokens = [int(token) for token in payload_in[10:-1].split()]
    color = (tokens[0], tokens[1], tokens[2])
    fill(color)
    return True

  if payload_in.startswith("(led:line "):
    tokens = [int(token) for token in payload_in[10:-1].split()]
    color = (tokens[0], tokens[1], tokens[2])
    line(color, tokens[3], tokens[4], tokens[5], tokens[6])
    return True

  if payload_in.startswith("(led:pixel "):
    tokens = [int(token) for token in payload_in[11:-1].split()]
    pixel((tokens[0], tokens[1], tokens[2]), tokens[3])
    return True

  if payload_in.startswith("(led:write"):
    tokens = [int(token) for token in payload_in[11:-1].split()]
    offset = 0
    for position in range(0, len(tokens) / 3):
      color = (tokens[offset], tokens[offset + 1], tokens[offset + 2])
      pixel(color, position)
      offset += 3
    np.write()
    return True

# if payload_in == "(led:traits)":
#   payload_out  = "(traits rgb " + str(LED_COUNT) + ")"
#   import aiko.mqtt
#   aiko.mqtt.client.publish(TOPIC_OUT, payload_out)
#   return True

  return False
