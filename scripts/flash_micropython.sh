#!/bin/bash
#
# Download microPython firmware from https://micropython.org/download
# Store in the ./firmware/ directory
#
# ./scripts/flash_micropython [esp32s3]
#
# To Do
# ~~~~~
# - Loop through list of known USB Serial device "/dev/tty*" paths ...
#   - Count number of devices and if there is one device, then use it
#   - Otherwise, display numeric index and devices allowing user to select one

# AMPY_PORT=/dev/tty.usbmodem14621   # Max OS X: Freetronics USB Serial adaptor
# AMPY_PORT=/dev/tty.SLAB_USBtoUART  # Mac OS X
# AMPY_PORT-/dev/ttyACM0  # Linux
# AMPY_PORT-/dev/ttyUSB0  # Linux

# BAUDRATE=115200
BAUDRATE=460800

CHIP=${1:-esp32}

# ESP32_MICROPYTHON=firmware/esp32-20210623-v1.16.bin
ESP32_MICROPYTHON=$CHIP-20220618-v1.19.1.bin

# ESP32_MICROPYTHON=firmware/esp32s3-generic-spiram-20220618-v1.19.1.bin

# ESP32-CAM
#### ESP32_MICROPYTHON=firmware/micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin
# ESP32_MICROPYTHON=firmware/micropython_camera_feeeb5ea3_esp32_idf4_4.bin

echo "### Erase flash: $CHIP ###"
esptool.py --chip $CHIP --no-stub --port $AMPY_PORT erase_flash

echo "### Flash microPython: $CHIP: $ESP32_MICROPYTHON ###"

if [ "x$CHIP" == "xesp32s3" ]; then
# ESP32 S3
  esptool.py --chip $CHIP --no-stub --port $AMPY_PORT --baud $BAUDRATE  \
      --before=default_reset --after=hard_reset  \
      write_flash -z 0x0 firmware/$ESP32_MICROPYTHON
else
# ESP32
  esptool.py --chip $CHIP --no-stub --port $AMPY_PORT --baud $BAUDRATE  \
      write_flash -z 0x1000 firmware/$ESP32_MICROPYTHON
fi

echo '### Complete ###'
