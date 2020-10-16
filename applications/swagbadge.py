# applications/swagbadge.py: version: 2020-10-17 04:00
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

def handler():
    pass

def initialise():
    event.add_timer_handler(handler, 100)
