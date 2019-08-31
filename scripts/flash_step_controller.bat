#!/bin/sh

set P=-p COM9 -d 1

echo "### Make directories ###"
ampy %P% mkdir applications
ampy %P% mkdir configuration
ampy %P% mkdir lib
ampy %P% mkdir lib/aiko
ampy %P% mkdir lib/umqtt

echo "### Copy applications/*.py ###"
ampy %P% put applications/step_controller.py applications/step_controller.py

echo "### Copy configuration/*.py ###"
ampy %P% put configuration/main.py      configuration/main.py
ampy %P% put configuration/led.py       configuration/led.py
ampy %P% put configuration/mqtt.py      configuration/mqtt.py
ampy %P% put configuration/net.py.cchs  configuration/net.py
ampy %P% put configuration/oled.py      configuration/oled.py
ampy %P% put configuration/services.py  configuration/services.py

echo "### Copy lib/aiko/*.py ###"
ampy %P% put lib/aiko/demonstration.py  lib/aiko/demonstration.py
ampy %P% put lib/aiko/event.py          lib/aiko/event.py
ampy %P% put lib/aiko/led.py            lib/aiko/led.py
ampy %P% put lib/aiko/mqtt.py           lib/aiko/mqtt.py
ampy %P% put lib/aiko/net.py            lib/aiko/net.py
ampy %P% put lib/aiko/oled.py           lib/aiko/oled.py
ampy %P% put lib/aiko/queue.py          lib/aiko/queue.py
ampy %P% put lib/aiko/services.py       lib/aiko/services.py

echo "### Copy ssd1306.py ###"
ampy %P% put lib/ssd1306.py lib/ssd1306.py

echo "### Copy threading.py ###"
ampy %P% put lib/threading.py lib/threading.py

echo "### Copy lib/umqtt ###"
ampy %P% put lib/umqtt/simple.py lib/umqtt/simple.py
ampy %P% put lib/umqtt/robust.py lib/umqtt/robust.py

echo "### Copy main.py ###"
ampy %P% put main.py main.py

echo "### Complete ###"
