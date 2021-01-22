# applications/swagbadge.py: version: 2020-12-27 14:00 v05
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

from aiko.common import convert_time
import aiko.event
import aiko.oled

titles = ["SwagBadge", "LCA2021"]
title_index = 0

timer = 0

def swagbadge_handler():
    global timer
    hours, minutes, seconds = convert_time(timer)
    timer += 1
    text = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    screen = aiko.oled.oleds[0]
    screen.fill_rect(0, 16, 128, 8, 0)
    screen.text(text, 0, 16)
    screen.show()

def swagbadge_title():
    global title_index
    aiko.oled.set_title(titles[title_index])
    aiko.oled.write_title()
    title_index = 1 - title_index

def initialise():
    aiko.event.add_timer_handler(swagbadge_handler, 1000, immediate=True)
    aiko.event.add_timer_handler(swagbadge_title, 5000)
