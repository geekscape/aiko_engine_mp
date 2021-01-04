# examples/oled_eyes.py
#
# Draw eyes on SwagBadge oleds
# Based on examples from aiko_engine_mp

# Usage
# ~~~~~
# Connect to SwagBadge with (something like) mpfshell
#   $ mpfshell -o ttyUSB0
# Upload this file, and run the code
#   mpfs [/]> put examples/oled_eyes.py
#   mpfs [/]> repl
#   MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
#   Type "help()" for more information.
#   >>> import examples.oled_eyes as eyes
#   >>> eyes.run()
#
# The software may take a few seconds to load and draw.
#
# To Do
# ~~~~~

import uos

import aiko.event as event
import aiko.oled as oled

import math

oled0 = oled.oleds[0]  # Left Eye
oled1 = oled.oleds[1]  # Right Eye

# offset = oled.font_size
# Assume left and right oleds are same size.
height = oled0.height
width = oled0.width

# Utilities
def random(min, max, r_max=255):
    r = uos.urandom(1)[0] & r_max
    r = r / r_max * (max - min) + min
    if r >= max:
        r = min
    return int(r)

def random_position(limit):
    limit = limit // 4
    return random(limit, limit * 3)

#
def new_eyes():
    global eye_position
    eye_position = (random_position(width), random_position(height))

def display_eyes():
    x0 = 60
    y0 = 40
    r = 20
    r2 = r*r
    for x in range(-1 * r, r):
        dh = math.ceil( math.sqrt( r2 - x*x ))
        for y in range(-1 * dh, dh):
            oled0.pixel(x+x0,y+y0,1)
            oled1.pixel(x+x0,y+y0,1)

def update_eyes():
    oled0.pixel(0,0,1)

def timer_handler():
    update_eyes()

def run(period=50):
    oled.oleds_clear(0)

    new_eyes()
    display_eyes()

    event.add_timer_handler(timer_handler, period)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(timer_handler)
