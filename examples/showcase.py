# examples/showcase.py
#
# Displays the status of the various switches and buttons
# Demonstrates how to programmatically access all the things.
#
# Usage
# ~~~~~
# import examples.showcase as showcase
# showcase.initialise()
# showcase.run()
#

from machine import Pin, TouchPad
import aiko.event as event
import aiko.oled as oled
import aiko.net as net 
import aiko.mqtt as mqtt
import aiko.led as led
import configuration.main

titles = ["SwagBadge", "LCA2021"]
title_index = 0


parameter = configuration.main.parameter



# Touchpad sliders 
# Left slider is pins 12 and 15, Right slider is pins 14 and 27
bottom_left = TouchPad(Pin(12))
top_left = TouchPad(Pin(15))
bottom_right = TouchPad(Pin(14))
top_right = TouchPad(Pin(27))

# Buttons!
button_left = Pin(16, Pin.IN, Pin.PULL_UP)
button_right = Pin(17, Pin.IN, Pin.PULL_UP)

# Turn a slider value into a human readable version
def slider_range(val):
  if val <= 30 and val >= -30:
    return "--"
  elif val < -30:
    return "/\\"
  elif val > 30: 
    return "\\/"
  return "off"
  
# Read the value of the sliders and burp them out in an array.  
def touch_slider_handler():
  # left slider
  left_slider = top_left.read() - bottom_left.read()
  
  # right slider
  right_slider = top_right.read() - bottom_right.read()

  # return where they're at, up, down or nothing.
  values = [slider_range(left_slider), slider_range(right_slider)]
  return values
  
# Display a rotating title  
def titlebar():
    global title_index
    oled.set_title(titles[title_index])
    oled.write_title()
    title_index = 1 - title_index

# Clean out the whole line that was there before
# Write some new text and show it
def oled_write_line(oled_target, x, y, text):
    oled_target.fill_rect(0,y,oled.width, oled.font_size, oled.bg)
    oled_target.text(text, x, y)
    
def statusbar():
# If oleds are enabled, then display a bunch of stuff to screen
# Send stuff to console log regardless:
# Wifi status icon
# MQTT status icon
# Button press status
    sliders = touch_slider_handler()
    if len(oled.oleds) > 0:
        oledL = oled.oleds[0]
        oledR = oled.oleds[1]
        oled_write_line(oledL, 1, 10, "Wifi: "+str(net.is_connected()))
        oled_write_line(oledL, 1, 20, "MQTT: "+str(mqtt.is_connected()))
        oled_write_line(oledL, 1, 30, " "+str(int(not(button_left.value())))+" Button "+str(int(not(button_right.value()))))
        oled_write_line(oledL, 1, 40, str(sliders[0])+" Slider "+str(sliders[1]))
        oledR.invert(1)
        oledR.fill(1)
        image = oled.load_image("../examples/tux_nice.pbm")
        oledR.blit(image,0,0)
        oled.oleds_show()
    else:
        print("No oleds present")
        print("Wifi: "+str(net.is_connected()))
        print("MQTT: "+str(mqtt.is_connected()))
        print(" "+str(int(not(buttonL.value())))+" Button "+str(int(not(buttonR.value()))))
        print(str(sliders[0])+" Slider "+str(sliders[1]))        
        

# Don't update the title bar too often
# But check on the status of the badge hardware and display that more frequently            
def run():
    oled.oleds_clear(0)
#    mqtt.initialise()
    event.add_timer_handler(titlebar, 5000)
    event.add_timer_handler(statusbar, 500)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(titlebar)
        event.remove_timer_handler(statusbar)


def initialise():
    led.initialise()
    oled.initialise()
    net.initialise()
    mqtt.initialise()
