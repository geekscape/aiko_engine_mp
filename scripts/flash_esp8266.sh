#!/bin/sh

AMPY_PORT=/dev/tty.usbmodem14621  # Freetronics USB Serial adaptor

echo '### Erase flash ###'
esptool.py --chip esp8266 --port $AMPY_PORT erase_flash

echo '### Flash microPython ###'
esptool.py --chip esp8266 --port $AMPY_PORT --baud 115200 write_flash --flash_size=detect 0 firmware/esp8266-20180602-v1.9.4-113-g7d86ac6c.bin
