# Example Code for LCA SwagBadge2021.
#
# Used to control a rumble motor to give @Enderboi a COVID-safe virtual handshake:
#
#
# on_shake_message():   # Badge-as-server
#    - Listen for '($shake_CMD $interval)' messages on MQTT, where $interval is user input
#    - Trigger an SAO pin ($shake_GPIO) for $interval microseconds if command recieved
#
# on_shake_slider()     # Badge-as-client
#    - Read 'intensity' of badges left capacitive touch slider
#    - Send a MQTT message of '($shake_CMD $INTENSITY)' to a predefined badge ($shake_TARGET)
#      (default hardcoded value is @Enderboi's - give him a virtual handshake!)
#
# on_shake_init()
#   - Register the above two handlers

import machine
import network
import usocket

import aiko.common
import aiko.mqtt
import aiko.button
import aiko.oled

from machine import Pin
from time import sleep_ms
from aiko.common import map_value

# Configuration
shake_GPIO = 25
shake_CMD = "shake"
shake_TARGET = "public/esp32_10521c5de398/0/in"
shake_lastSliderVal = 0

# on_shake_message() - Receive Badge Handshake
def on_shake_message(topic, payload_in):
    if payload_in != "nil":
        tokens = payload_in[1:-1].split()
    if tokens[0] == "shake":
        motor = Pin(shake_GPIO, Pin.OUT, Pin.PULL_UP)
        print("[Shake] Received Shake Command. Triggering GPIO {} for {}ms".format(shake_GPIO, int(tokens[1])))
        aiko.mqtt.client.publish(topic, "Shake Intensity: {}".format(int(tokens[1])))
        motor.on()
        sleep_ms(int(tokens[1]))
        motor.off()
    return True

# on_shake_slider() - Transmit Badge Handshake
def on_shake_slider(pin_number, state, value):
    print("Slider Pin {} = {} (State: {})".format(pin_number, value, state))

    screen = aiko.oled.oleds[0]

    if screen:
        text = "Send Handshak\n   Interval?"
        aiko.oled.oleds_clear()
        screen.fill_rect(0, 32, 128, 8, 0)
        screen.text(text, 0, 32)
        if value:
            value = int(map_value(value, 0, 100, 0, 128))
            screen.fill_rect(0, 48, 128, 16, 0)
            screen.fill_rect(0, 48, value, 16, 1)
        screen.show()

    if state == 1:
       shake_lastSliderVal = int(value)

    if state == 2:
        print("Last value was: {}".format(shake_lastSliderVal))
        aiko.oled.oleds_log("Sending Shake @ {}%!".format(shake_lastSliderVal))
        sleep_ms(250)
        aiko.oled.oleds_log("Hand SHOOK!")
        sleep_ms(1000)
        aiko.oled.oleds_clear()
        shake_lastSliderVal = 0

# on_shake_init() - Register both above handlers
def on_shake_init():
    aiko.mqtt.add_message_handler(on_shake_message)
    aiko.button.add_slider_handler(on_shake_slider, 12, 15)
    print("[Shake] Plugin Registered")

# ... Acknowledge we loaded the .py without any syntax errors, for debugging purpoes :D
print("[Shake] Plugin Loaded")

# Actually init the module and register handlers
on_shake_init()

