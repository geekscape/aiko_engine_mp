# INSTALL requirements
# pip install requests
#

import requests
import json
from datetime import timedelta, datetime

# Sender: read json from lca website
# while the current time is before Monday night
#     if there is a talk coming up in the next 1 minutes?
#         Put out a message on a queue of the same name as the room (lca/schedule/<room>, with now flag, talk title, speaker name
#     else if there is a talk coming up in the next 10 minutes?
#         Put out a message on a queue of the same name as the room, with upcoming flag, talk title, speaker name
#     wait 1 minutes
#     

# response = requests.get("https://linux.conf.au/schedule/conference.json")
# responsetext = json.loads(response.text)

with open("schedule.json") as file:
    data = json.load(file)
    
upcomingdelta = timedelta(days=1,hours=12,minutes=10)
nowdelta = timedelta(minutes=1)
rightnow = datetime.now()

print(rightnow+upcomingdelta)
for id in data['schedule']:
    starttime = datetime.fromisoformat(id['start'])
    if (id['kind'].lower() == "break") or (id['kind'].lower() == "room changeover") \
        or (id['kind'].lower() == "morning tea") or (id['kind'].lower() == "lunch") \
        or (('cancelled' in id) and (id['cancelled'])):
        continue
    if rightnow < starttime and rightnow + nowdelta > starttime:
        print("starting now")
    elif rightnow < starttime and rightnow + upcomingdelta > starttime:
        print("coming up: "+starttime.strftime('%a %I:%M %S %p'))
    else:
        continue
    print("  Room: "+id['room'])
    print("  "+id['name'])
    if 'authors' in id:
        print("  "+id['authors'][0]['name'])
        
#        print("skipping")
#        print(id)
        
