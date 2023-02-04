#!/bin/bash

AMPY_PORT=/dev/tty.usbmodem14621  # Freetronics USB Serial adaptor
# BAUDRATE=115200
BAUDRATE=460800

ESP32_MICROPYTHON=firmware/esp8266-20180602-v1.9.4-113-g7d86ac6c.bin

echo '### Erase flash ###'
esptool.py --chip esp8266 --port $AMPY_PORT erase_flash

echo '### Flash microPython ###'
esptool.py --chip esp8266 --port $AMPY_PORT --baud $BAUDRATE write_flash --flash_size=detect 0 $ESP32_MICROPYTHON
