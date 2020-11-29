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
#
from machine import Pin, TouchPad
import aiko.event as event
import aiko.oled as oled
import framebuf


titles = ["SwagBadge", "LCA2021"]
title_index = 0

import aiko.net as net
import aiko.mqtt as mqtt

import configuration.main
parameter = configuration.main.parameter

touch5 = TouchPad(Pin(12))
touch3 = TouchPad(Pin(15))

touch6 = TouchPad(Pin(14))
touch7 = TouchPad(Pin(27))

buttonR = Pin(17, Pin.IN, Pin.PULL_UP)
buttonL = Pin(16, Pin.IN, Pin.PULL_UP)

if parameter("oled_enabled"):
    import aiko.oled as oled


def load_image(filename):
    with open(filename, 'rb') as file:
        file.readline()  # magic number: P4
        file.readline()  # creator comment
        width, height = [int(value) for value in file.readline().split()]
        image = bytearray(file.read())
    return framebuf.FrameBuffer(image, width, height, framebuf.MONO_HLSB)


# Turn a slider value into a human readable version
def slider_range(val):
  if val <= 30 and val >= -30:
    return "--"
  elif val < -30:
    return "/\\"
  elif val > 30: 
    return "\\/"
  return "off"
  
def touch_slider_handler():
  # left slider
  value0 = touch5.read()
  value1 = touch3.read()
  value0 = value1 - value0
  
  # right slider
  value2 = touch6.read()
  value3 = touch7.read()
  value2 = value3 - value2

  # return where they're at, up, down or nothing.
  values = [slider_range(value0), slider_range(value2)]
  return values
  
def handler():
    global title_index
    oled.set_title(titles[title_index])
    oled.write_title()
    title_index = 1 - title_index

def oled_write_line(oled_target, x, y, text):
    oled_target.fill_rect(0,y,oled.width, oled.font_size, oled.bg)
    oled_target.text(text, x, y)
    oled_target.show()
    
def statusbar():
# If oleds are enabled, then display a bunch of stuff to screen
# Send stuff to console log regardless:
# Wifi status icon
# MQTT status icon
# Button press status
    sliders = touch_slider_handler()
    if parameter("oled_enabled"):
        oledL = oled.oleds[0]
        oledR = oled.oleds[1]
        oled_write_line(oledL, 1, 10, "Wifi: "+str(net.is_connected()))
        oled_write_line(oledL, 1, 20, "MQTT: "+str(mqtt.is_connected()))
        oled_write_line(oledL, 1, 30, " "+str(int(not(buttonL.value())))+" Button "+str(int(not(buttonR.value()))))
        oled_write_line(oledL, 1, 40, str(sliders[0])+" Slider "+str(sliders[1]))
        oledR.invert(1)
        oledR.fill(1)
        tux_64 = load_image("../examples/tux_nice.pbm")
        oledR.blit(tux_64, 0, 0)
        oledR.show()
            
def initialise():
    event.add_timer_handler(handler, 5000)
    event.add_timer_handler(statusbar, 500)
