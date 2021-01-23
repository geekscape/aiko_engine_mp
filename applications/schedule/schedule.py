# applications/schedule.py
#
# Displays alerts when the next LCA2021 event is about to start
#
# Usage
# ~~~~~
# TODO

from machine import Pin, TouchPad
import aiko.event as event
import aiko.oled as oled
import aiko.mqtt as mqtt
import configuration.schedule
import aiko.common as common

titles = ["SwagBadge", "LCA2021", "Schedule"]
title_index = 0


schedule = None

# Display a rotating title
def titlebar():
    global title_index
    oled.set_title(titles[title_index])
    oled.write_title()
    title_index = (title_index + 1) % len(titles)


# Clean out the whole line that was there before
# Write some new text and show it
def oled_write_line(oled_target, x, y, text):
    oled_target.fill_rect(0,y,oled.width, oled.font_size, oled.bg)
    oled_target.text(text, x, y)


# (session:##[upcoming <time>|now]##title:<title>##speaker:<speaker>##room:<room>)
def on_schedule_message(topic,payload_in):
    when,title,speaker, room = "", "", "", ""
    if payload_in.startswith("(session:"):
        talk = payload_in[9:-1]
        tokenised = talk.split("##")
#        print(tokenised)
        for token in tokenised:
            if token.startswith("title:"):
                title = token[6:]
            elif token.startswith("speaker:"):
                speaker = token[8:]
            elif token == "now":
                when = "now"
            elif token.startswith("upcoming "):
                when = token[9:]
            elif token.startswith("room:"):
                room = token[5:]
            else:
                pass
#        print("topic "+topic)
        if (topic.endswith("break")):
#            print(when+" "+title)
            oled.oleds_log(when+" "+title)
        else:
#            print(when+" "+title+" "+speaker+" "+room)
            oled.oleds_log(when+" "+title)
            oled.oleds_log(" "+speaker+" "+room)
        return True
    return False


# Don't update the title bar too often
# But check on the status of the badge hardware and display that more frequently
def initialise():
    global schedule,menu

    schedule = configuration.schedule.settings
    oled.oleds_clear(oled.BG)
    event.add_timer_handler(titlebar, 5000)
    prefix = configuration.schedule.settings['topicprefix']

    for topic in configuration.schedule.settings['topics']:
        mqtt.add_message_handler(on_schedule_message, prefix+topic)

def finalise():
    event.remove_timer_handler(titlebar)

# Badge: read config from file (default all)
# on init set message handlers to monitor lca/schedule/<room> as configured
# when handler fires, display on screen
