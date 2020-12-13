# applications/swagbadge.py: version: 2020-12-13 18:00 v03
#
# Usage
# ~~~~~
# import applications.swagbadge as demo
#
# To Do
# ~~~~~
# - Implement dual OLED screen support
# - Implement buttons
# - Implement touch sliders
# - Implement Messaging (secure)
# - Implement SAO handling
# - Implement Out-Of-The-Box experience

import aiko.event as event
import aiko.oled as oled

titles = ["SwagBadge", "LCA2021"]
title_index = 0

def swagbadge_handler():
    global title_index
    oled.set_title(titles[title_index])
    oled.write_title()
    title_index = 1 - title_index

def initialise():
    event.add_timer_handler(swagbadge_handler, 5000)
