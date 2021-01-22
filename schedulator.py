# INSTALL requirements
# pip install requests
# pip install paho-mqtt
#

import requests
import json
from datetime import timedelta, datetime
import time
from paho.mqtt import client as mqtt

# Sender: read json from lca website
# while the current time is before Monday night
#     if there is a talk coming up in the next 1 minutes?
#         Put out a message on a queue of the same name as the room (lca/schedule/<room>, with now flag, talk title, speaker name
#     else if there is a talk coming up in the next 10 minutes?
#         Put out a message on a queue of the same name as the room, with upcoming flag, talk title, speaker name
#     wait 1 minutes
#     

# MQTT channel settings
topicprefix = "public/lca/schedule/"
breaktopic = topicprefix+"breaks"
# each room gets its own topic, pulled from the schedule data

broker = '101.181.46.180'
port = 1883
client_id = 'LCA2021 schedulator'

# A session is upcoming if it's within 10 minutes (values vary during testing)  
upcomingdelta = timedelta(hours=19,minutes=10)
# A session is on right now if it's within 1 minute
nowdelta = timedelta(minutes=1)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    

def send_message(client, topic, msg):
    print("publishing "+topic+" // "+msg)
    result = client.publish(topic, msg)
    print("ok")
    # result: [0, 1]
    status = result[0]
    if status != 0:
        print("Failed to send message to topic "+topic)
        
        
client = connect_mqtt()
client.loop_start()

# (session:##[upcoming <time>|now]##title:<title>##speaker:<speaker>##room:<room>)

while (datetime.now() < datetime.fromisoformat("2021-01-25T23:59:59")):
    rightnow = datetime.now()
    
    # When live, have the schedulator pull the schedule from the conf website.
    # Dunno if we poll every minute, or use a local cache for an hour
    # Or just stick with a static daily dump
    # response = requests.get("https://linux.conf.au/schedule/conference.json")
    # responsetext = json.loads(response.text)

    # In testing, we just use a local file copy to draw on
    with open("schedule.json") as file:
        data = json.load(file)
        
    for id in data['schedule']:
        message = "(session:"
        starttime = datetime.fromisoformat(id['start'])
        # Don't alert for cancelled sessions
        if (('cancelled' in id) and (id['cancelled'])):
            continue

        # Set the room topic. Currently supported:
        # - break
        # - an attempt to normalise the room name data (strip spaces or full stops)
        if (id['kind'].lower() == "break") or (id['kind'].lower() == "room changeover") \
            or (id['kind'].lower() == "morning tea") or (id['kind'].lower() == "lunch"):
            roomtopic="break"
        else:
            roomtopic = id['room'].lower().replace(" ","").replace(".","")
            
        # When is the session?
        # - is it on now?
        # - coming soon?
        # - historical or sufficiently in the future that we don't care - skip
        if rightnow < starttime and rightnow + nowdelta > starttime:
            print("starting now")
            message += "##now"
        elif rightnow < starttime and rightnow + upcomingdelta > starttime:
            print("coming up: "+starttime.strftime('%a %I:%M %p'))
            message += "##upcoming "+starttime.strftime('%a %I:%M')
        else:
            continue
        
        # We have enough to proceed
        print("  Room: "+id['room'])
        print("  "+id['name'])
        message += "##title:"+id['name']+"##room:"+id['room']
        # sorry sessions with multiple authors
        if 'authors' in id:
            print("  "+id['authors'][0]['name'])
            message += "##speaker:"+id['authors'][0]['name']
        message +=")"

        send_message(client,topicprefix+roomtopic,message)
    
    # pause for a minute and do it all again
    print("\n sleeping\n")
    time.sleep(60)
            

