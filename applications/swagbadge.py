# applications/swagbadge.py: version: 2023-03-11 14:00 v06
#
# To Do
# ~~~~~
# - Implement buttons
# - Implement touch sliders
# - Implement Messaging (secure)
# - Implement SAO handling
# - Implement Out-Of-The-Box experience
#   - Put the "images" onto the flash filesystem
#   - Randomly select 10 images
#   - Slide them across the OLED screen
#   - Display Christmas / New Year greeting !
#   - Repeat :)

import gc
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont

from aiko.common import convert_time
import aiko.event

titles = ["SwagBadge", "EO2023"]
title_index = 0

display = None
font = None
fg = 0
bg = 0
timer = 0

def swagbadge_handler():
    global display, font, fg, bg, timer
    print("Before: " + str(gc.mem_free()))
    gc.collect()
    hours, minutes, seconds = convert_time(timer)
    timer += 1
    text = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    display.draw_text(64, 0, text, font, fg, background=bg)
    gc.collect()
    print("After:  " + str(gc.mem_free()))

def swagbadge_title():
    global title_index
    aiko.oled.set_title(titles[title_index])
    aiko.oled.write_title()
    title_index = 1 - title_index

def initialise():
    global display, font, fg, bg

    gc.collect()
    Pin(2, Pin.OUT).value(1)
    spi = SPI(1, baudrate=20000000, sck=Pin(14), mosi=Pin(26))
    display = Display(spi, dc=Pin(25), cs=Pin(16), rst=Pin(17),
        width=320, height=240, rotation=90)
    font = XglcdFont("fonts/Bally7x9.c", 7, 9)
    gc.collect()

    fg = color565(0, 255, 0)
    bg = color565(0, 96, 48)
    display.clear(bg)
    display.fill_polygon(6, 160, 120, 80, color565(255, 0, 0))
    for y in range(0, 100, 10):
        display.draw_text(0, y, "hello", font, fg, background=bg)
    gc.collect()
#   display.cleanup()

    aiko.event.add_timer_handler(swagbadge_handler, 1000, immediate=True)
#   aiko.event.add_timer_handler(swagbadge_title, 5000)
