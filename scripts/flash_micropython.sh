#!/bin/sh
#
# To Do
# ~~~~~
# - Loop through list of known USB Serial device "/dev/tty*" paths ...
#   - Count number of devices and if there is one device, then use it
#   - Otherwise, display index / devices allowing user to select one

# AMPY_PORT=/dev/tty.usbmodem14621  # Freetronics USB Serial adaptor
# AMPY_PORT=/dev/tty.SLAB_USBtoUART

# BAUDRATE=115200
BAUDRATE=460800

# ESP32_MICROPYTHON=firmware/esp32-idf4-20200902-v1.13.bin
ESP32_MICROPYTHON=firmware/esp32-20210623-v1.16.bin

if [ ! -f firmware/$ESP32_MICROPYTHON ]; then
    mkdir -p firmware
    curl -Lo $ESP32_MICROPYTHON https://micropython.org/resources/$ESP32_MICROPYTHON
fi

echo '### Erase flash ###'
esptool.py --chip esp32 --port $AMPY_PORT erase_flash

echo '### Flash microPython ###'
esptool.py --chip esp32 --port $AMPY_PORT --baud $BAUDRATE write_flash -z 0x1000 $ESP32_MICROPYTHON

echo '### Complete ###'
