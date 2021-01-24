# Ender's Example PLugin for LCA SwagBadge2021
#
# Used to control a rumble motor to give @Enderboi a COVID-safe virtual handshake:
#     - https://twitter.com/Enderboi/status/1352807738707857408   <-- Prototype HW Implementation? :P
#
# on_shake_message():   # Badge-as-server
#    - Listen for '($shake_CMD $interval $id)' messages on MQTT
#      ... where $interval is user input and $id is optional sender badge serial (or custom identifier)
#    - Trigger an SAO pin ($shake_GPIO) for $interval microseconds if command recieved
#
# on_shake_slider()     # Badge-as-client
#    - Read 'intensity' of badges left capacitive touch slider
#    - Send a MQTT message of '($shake_CMD $interval $badge_id)' to a predefined badge ($shake_TARGET)
#      ... (default hardcoded value is @Enderboi's - give him a virtual handshake!)
#
# on_shake_ui()         # Draw and enable the UI, including *magic* for when called via the System UI menu
# draw_progressbar()    # Moar Graphics (UI helper)
#
# on_shake_init()
#   - Register the above two handlers

import machine
import network
import usocket
import binascii

import aiko.common
import aiko.mqtt
import aiko.button
import aiko.oled
import aiko.system_ui

from machine import Pin
from time import sleep_ms
from aiko.common import map_value
from aiko import oled

# Configuration
shake_GPIO = 25   # For SwagBadge2021, GPIO25 maps to IO2 on SAO4
shake_CMD = "shake"
shake_TARGET = "public/esp32_10521c5de398/0/in"   # Default Target: Ender's Hand -  See https://twitter.com/Enderboi/status/1352807738707857408
shake_lastSliderVal = 0
shake_SOURCE = binascii.hexlify(machine.unique_id())

# on_shake_message() - Receive Badge Handshake and trigger a GPIO in response (this is the server part of the example)
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

# Draw a percentile progress/slider bar
def draw_progressbar(screen, value):
    screen = oled.oleds[screen]
    screen.fill_rect(0, 32, 128, 8, 0)
    if value:
        value = int(map_value(value, 0, 100, 0, 128))
        screen.fill_rect(0, 48, 128, 16, 0)
        screen.fill_rect(0, 48, value, 16, 1)
    screen.show()

def on_shake_ui():
    # Disable System UI if that's what called me... otherwise we can't use nice things
    if aiko.system_ui.system_ui_active:
      print("[Shake] Called from System UI - disabling")
      aiko.system_ui.system_features_handler(1)

    # Clear the screen and draw the title
    oled.oleds_clear()
    oled.oleds_text("  Slide Left      To Shake!  ", 0, 14, 1)

    # The title takes a second to raster onto the second screen, to a little sleep_ms here for UI experience :)
    sleep_ms(250)

    # Register our slider handler
    aiko.button.add_slider_handler(on_shake_slider, 12, 15)

# on_shake_slider() - Transmit Badge Handshake and show a little UI (basically the client bit of this example)
def on_shake_slider(pin_number, state, value):
    global shake_lastSliderVal, shake_SOURCE, shake_TARGET

    # Update the UI strength bar
    draw_progressbar(0, value)

    # If we're still dragging (state == 1), record latest value
    if state == 1:
        shake_lastSliderVal = value

    # Once finger has been released (state == 2), use the last value for sending the trigger message, then
    # show a little UI animation while resetting the stored value for the next use :)
    if state == 2 and shake_lastSliderVal > 0:
        # Send the MQTT trigger (shake) message
        print("MQTT Send {}: (shake {} {})".format(shake_TARGET, shake_lastSliderVal * 100, shake_SOURCE))
        aiko.mqtt.client.publish(shake_TARGET, "(shake {} {})".format(shake_lastSliderVal * 30, shake_SOURCE))

        # ... also display a little UI animation for fun
        oled.oleds_clear()
        oled.oleds_text(" Sending Shake!    {}% POWER!".format(shake_lastSliderVal), 0, 14, 1)
        shake_lastSliderVal = 0                      # (... oh, and don't forget to reset the slider value store)
        aiko.button.remove_handler(on_shake_slider)  # and unregister our slider control!

        for screen in range(0, 2):
           for x in range(0, 20):
              draw_progressbar(screen, x*5)
              sleep_ms(20)
        oled.oleds_text("   HANDSHAKE      COMPLETE", 0, 32, 1)

        # Clear display after 8s to prevent messy overwriting
        sleep_ms(8000)
        oled.oleds_clear()

# on_shake_init() - Register both above handlers
def on_shake_init():
    # Register to receive activation messages for a motor
    aiko.mqtt.add_message_handler(on_shake_message)

    # We can just register us on the System Menu (default)
    aiko.system_ui.features.append(('Send Handshake', on_shake_ui))
    aiko.system_ui.menu_items = len(aiko.system_ui.features)

    # .. or activate if we click the left screen (not default :)
    # aiko.button.add_button_handler(on_shake_ui, [16])   

    # All done for on_shake_init()
    print("[Shake] Plugin Registered")

#############################################################
# sudo make me a coffee

# ... For troubleshooting purposes, let's ack if the file was actually loaded and parsed to this point :)
print("[Shake] Plugin Loaded")

# And lastly, the main even! Let's init this plugin and register our action handlers with Aiko
on_shake_init()

