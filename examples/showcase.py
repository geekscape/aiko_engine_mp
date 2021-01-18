# examples/showcase.py: version: 2021-01-19 07:00
#
# Displays the status of the various switches and buttons
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/showcase.py
# mpfs [/]> put examples/tux_nice.pbm
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> from examples.showcase import run
# >>> run()

from machine import Pin, TouchPad

import aiko.event
import aiko.mqtt
import aiko.net
import aiko.oled as oled

button_left = Pin(16, Pin.IN, Pin.PULL_UP)
button_right = Pin(17, Pin.IN, Pin.PULL_UP)

bottom_left = TouchPad(Pin(12))
top_left = TouchPad(Pin(15))
bottom_right = TouchPad(Pin(14))
top_right = TouchPad(Pin(27))

# Turn a slider value into a human readable version

def slider_range(val):
  if val <= 30 and val >= -30:
    return "--"
  elif val < -30:
    return "/\\"
  elif val > 30: 
    return "\\/"
  return "off"
  
# Read the value of the sliders and return them in an array.  

def touch_slider_handler():
  left_slider = top_left.read() - bottom_left.read()
  right_slider = top_right.read() - bottom_right.read()

  # return where they're at, up, down or nothing.
  values = [slider_range(left_slider), slider_range(right_slider)]
  return values
  
# Clean out the whole line that was there before
# Write some new text and show it

def oled_write_line(oled_target, x, y, text):
    oled_target.fill_rect(0, y, oled.width, oled.font_size, oled.bg)
    oled_target.text(text, x, y)
    
# If OLED screens are enabled, then display ...
# - Wifi status
# - MQTT status
# - OLED screens button press status
# - Touch slider status
# - Penguin picture

image = oled.load_image("examples/tux_nice.pbm")

def status_handler():
    sliders = touch_slider_handler()
    if len(oled.oleds) > 0:
        oledL = oled.oleds[0]
        oledR = oled.oleds[1]

        oled_write_line(oledL, 1, 10, "Wifi: "+str(aiko.net.is_connected()))
        oled_write_line(oledL, 1, 20, "MQTT: "+str(aiko.mqtt.is_connected()))
        oled_write_line(oledL, 1, 30, " "+str(int(not(button_left.value())))+" Button "+str(int(not(button_right.value()))))
        oled_write_line(oledL, 1, 40, str(sliders[0])+" Slider "+str(sliders[1]))
        oledR.invert(1)
        oledR.fill(1)
        oledR.blit(image,0,0)
        oled.oleds_show()
    else:
        print("No OLED screens found")

def run():
    oled.oleds_clear(0)
    aiko.event.add_timer_handler(status_handler, 500, immediate=True)
