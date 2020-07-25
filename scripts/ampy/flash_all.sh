#!/bin/sh

# AMPY_PORT=/dev/tty.usbmodem14621  # Freetronics USB Serial adaptor
# AMPY_PORT=/dev/tty.SLAB_USBtoUART

# BAUDRATE=115200
BAUDRATE=460800

ESP32_MICROPYTHON=firmware/esp32-idf4-20191220-v1.12.bin

echo '### Erase flash ###'
esptool.py --chip esp32 --port $AMPY_PORT erase_flash

echo '### Flash microPython ###'
esptool.py --chip esp32 --port $AMPY_PORT --baud $BAUDRATE write_flash -z 0x1000 $ESP32_MICROPYTHON

echo '### Make directories ###'
ampy mkdir applications
ampy mkdir applications/step_patterns
ampy mkdir configuration
ampy mkdir lib
ampy mkdir lib/aiko
ampy mkdir lib/umqtt

echo '### Copy applications/*.py ###'
# ampy put applications/nodebots.py applications/nodebots.py
ampy put applications/step_controller.py applications/step_controller.py
ampy put applications/step_patterns/cchs_1.py applications/step_patterns/cchs_1.py
ampy put applications/step_patterns/skipping_girl.py applications/step_patterns/skipping_girl.py

echo '### Copy configuration/*.py ###'
ampy put configuration/main.py      configuration/main.py
ampy put configuration/led.py       configuration/led.py
ampy put configuration/lolibot.py   configuration/lolibot.py
ampy put configuration/mqtt.py      configuration/mqtt.py
ampy put configuration/net.py       configuration/net.py
ampy put configuration/oled.py      configuration/oled.py
ampy put configuration/services.py  configuration/services.py

echo '### Copy lib/aiko/*.py ###'
ampy put lib/aiko/demonstration.py  lib/aiko/demonstration.py
ampy put lib/aiko/event.py          lib/aiko/event.py
ampy put lib/aiko/led.py            lib/aiko/led.py
ampy put lib/aiko/mqtt.py           lib/aiko/mqtt.py
ampy put lib/aiko/net.py            lib/aiko/net.py
ampy put lib/aiko/oled.py           lib/aiko/oled.py
ampy put lib/aiko/queue.py          lib/aiko/queue.py
ampy put lib/aiko/services.py       lib/aiko/services.py

# echo '### Copy lolibot.py ###'
# ampy put lib/lolibot.py lib/lolibot.py

echo '### Copy mpu9250.py ###'
ampy put lib/mpu9250.py lib/mpu9250.py

echo '### Copy ssd1306.py ###'
ampy put lib/ssd1306.py lib/ssd1306.py

echo '### Copy threading.py ###'
ampy put lib/threading.py lib/threading.py

echo '### Copy lib/umqtt ###'
ampy put lib/umqtt/simple.py lib/umqtt/simple.py
ampy put lib/umqtt/robust.py lib/umqtt/robust.py

# echo '### Copy play.py ###'
# ampy put play.py play.py

echo '### Copy main.py ###'
ampy put main.py main.py

echo '### Complete ###'

# screen $AMPY_PORT 115200
