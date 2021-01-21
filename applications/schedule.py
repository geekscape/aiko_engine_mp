# applications/schedule.py
#
# Displays alerts when the next LCA2021 event is about to start
#
# Usage
# ~~~~~
# TODO
#

from machine import Pin, TouchPad
import aiko.event as event
import aiko.oled as oled
import aiko.net as net 
import aiko.mqtt as mqtt
import configuration.schedule
import aiko.common as common
from time import sleep_ms

titles = ["SwagBadge", "LCA2021", "Schedule"]
title_index = 0

# Touchpad sliders 
# Left slider is pins 12 and 15, Right slider is pins 14 and 27
bottom_left = TouchPad(Pin(12))
top_left = TouchPad(Pin(15))
bottom_right = TouchPad(Pin(14))
top_right = TouchPad(Pin(27))

# Buttons!
button_left = Pin(16, Pin.IN, Pin.PULL_UP)
button_right = Pin(17, Pin.IN, Pin.PULL_UP)
downL = 12
upL = 15
downR = 14
upR = 27

schedule = None
selected = None
scrollerpos = 1
menu = None

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
    title_index = (title_index + 1) % len(titles)
    online_status['net'] = int(net.is_connected())
    online_status['mqtt'] = int(mqtt.is_connected())


# Clean out the whole line that was there before
# Write some new text and show it
def oled_write_line(oled_target, x, y, text):
    oled_target.fill_rect(0,y,oled.width, oled.font_size, oled.bg)
    oled_target.text(text, x, y)

# Display the items in a menu, highlighting the currently selected one      
def draw_menu(items):
    global scrollerpos
    i = 1

    oled.oleds_clear(oled.bg)
    bg = oled.bg
    fg = oled.fg
    
    for item in items:
        if i==scrollerpos:
            oled.oleds[0].fill_rect(0, 11*(i), 2*oled.font_size, oled.font_size, fg)
            oled.oleds_text(" >",0,11*(i), bg)
            oled.oleds_text(item, 2*oled.font_size, 11*(i), fg)
        else:
            for oleder in oled.oleds:
                oleder.fill_rect(0, 11*(i), oleder.width-10, oled.font_size, bg)
            oled.oleds_text("  "+item, 0, 11*(i), fg)
        i=i+1
    oled.oleds_text("Push screen to select",0,11*(i), fg)
    oled.oleds_show()
    
# (session:##[upcoming <time>|now]##title:<title>##speaker:<speaker>##room:<room>)
def on_schedule_message(topic,payload_in):
    when,title,speaker, room = None, None, None, None
    if payload_in.startswith("(session:"):
        talk = payload_in[9:-1]
        tokenised = talk.split("##")
        print(tokenised)
        for token in tokenised:
            if token.startswith("title:"):
                title = token[6:]
            elif token.startswith("speaker:"):
                speaker = token[8:]
            elif token == "now":
                when = "now"
            elif token.startswith("upcoming "):
                when = token[10:]
            elif token.startswith("room:"):
                room = token[5:]
            else:
                pass
        print(when+" "+title+" "+speaker+" "+room)
        oled.log(when+" "+title)
        oled.log(speaker+" "+room)
        return True    
    return False
    
# Don't update the title bar too often
# But check on the status of the badge hardware and display that more frequently            
def initialise():
    global schedule,menu
    
    schedule = configuration.schedule.format
    oled.oleds_clear(oled.bg)
    event.add_timer_handler(titlebar, 5000)

    mqtt.add_message_handler(on_schedule_message, "public/lca/schedule")

def finalise():
    event.remove_timer_handler(titlebar)




# Badge: read config from file (default all)
# on init set message handlers to monitor lca/schedule/<room> as configured
# when handler fires, display on screen