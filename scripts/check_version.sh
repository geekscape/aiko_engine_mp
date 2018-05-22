#!/bin/sh

ampy get main.py | grep version:
ampy get play.py | grep version:

ampy get lib/lolibot.py | grep version:

ampy get lib/aiko/demonstration.py | grep version:
ampy get lib/aiko/event.py         | grep version:
ampy get lib/aiko/led.py           | grep version:
ampy get lib/aiko/mqtt.py          | grep version:
ampy get lib/aiko/net.py           | grep version:
ampy get lib/aiko/oled.py          | grep version:
ampy get lib/aiko/queue.py         | grep version:
ampy get lib/aiko/services.py      | grep version:

ampy get configuration/main.py     | grep version:
ampy get configuration/led.py      | grep version:
ampy get configuration/lolibot.py  | grep version:
ampy get configuration/mqtt.py     | grep version:
ampy get configuration/net.py      | grep version:
ampy get configuration/oled.py     | grep version:
ampy get configuration/services.py | grep version:
