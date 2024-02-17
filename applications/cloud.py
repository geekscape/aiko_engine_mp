# applications/cloud.py: version: 2023-08-01 00:00 v00
#
# Usage
# ~~~~~
# import applications.cloud as cloud
#
# To Do
# ~~~~~
# - Don't hard code PIXEL_COUNT
#
# - Network and Message Transport state change handler manages application

import aiko.event as event
import aiko.led as led
import aiko.net as net

PIXEL_COUNT = 150  # Get configuration.led.settings["dimension"]

dot = 0
led_old = led.black

def handler_boot():  # TODO: Replace with proper state change handler
    if net.connected:
        event.remove_timer_handler(handler_boot)
        event.add_timer_handler(handler_led, 10)

def handler_led():
    global dot, led_old

    led.np[dot] = led_old
    dot = (dot + 1) % PIXEL_COUNT
    led_old = led.np[dot]
    led.np[dot] = led.white
    led.np.write()

def initialise():
   event.add_timer_handler(handler_boot, 1000)
