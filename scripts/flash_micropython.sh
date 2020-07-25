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

echo '### Complete ###'
