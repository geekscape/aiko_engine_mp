#!/bin/bash
#
# Download microPython firmware from https://micropython.org/download
# Store in the ./firmware/ directory
#
# Usage
# ~~~~~
# ESP32 S3 ROM doesn't support "esptool.py write_flash", so do this instead ...
#
# </dev/zero tr '\000' '\377' | head -c 8388608 >firmware/flash_0xff_8mb.bin
#
# esptool.py --chip esp32s3 --no-stub               \
#   --port $AMPY_PORT --baud $BAUDRATE              \
#   --before=default_reset --after=hard_reset       \
#   write_flash -z 0x0 firmware/flash_0xff_8mb.bin
#
# ./scripts/flash_micropython [esp32s3]
#
# To Do
# ~~~~~
# - Include ESP32 S3 workaround for "flash_erase" using "flash_0xff_8mb.bin"
#
# - Loop through list of known USB Serial device "/dev/tty*" paths ...
#   - Count number of devices and if there is one device, then use it
#   - Otherwise, display numeric index and devices allowing user to select one

# AMPY_PORT=/dev/tty.usbmodem14621   # Max OS X: Freetronics USB Serial adaptor
# AMPY_PORT=/dev/tty.SLAB_USBtoUART  # Mac OS X
# AMPY_PORT-/dev/ttyACM0             # Linux  ESP32 S3 Banana Pi Leaf S3
# AMPY_PORT-/dev/ttyUSB0             # Linux: ESP32 Wemos Lolin32 Lite

# BAUDRATE=115200
BAUDRATE=460800

CHIP=${1:-esp32}

# ESP32_MICROPYTHON=firmware/esp32-20210623-v1.16.bin
# ESP32_MICROPYTHON=$CHIP-20220618-v1.19.1.bin
ESP32_MICROPYTHON=$CHIP-20230426-v1.20.0.bin

# ESP32 S3: First working version (reliable and TouchPad):  Was after v1.20.0
# ESP32_MICROPYTHON=esp32s3-generic-spiram-20230426-v1.20.0-327-gd14ddcbdb.bin

# ESP32-CAM
#### ESP32_MICROPYTHON=firmware/micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin
# ESP32_MICROPYTHON=firmware/micropython_camera_feeeb5ea3_esp32_idf4_4.bin

echo "### Erase flash: $CHIP ###"
if [ "x$CHIP" == "xesp32s3" ]; then
# esptool.py --chip $CHIP --no-stub --port $AMPY_PORT erase_flash
# cat /dev/zero | tr '\000' '\377' | head -c 8388608 > flash_0xff_8mb.bin
  esptool.py --chip esp32s3 --no-stub               \
    --port $AMPY_PORT --baud $BAUDRATE              \
    --before=default_reset --after=hard_reset       \
    write_flash -z 0x0 firmware/flash_0xff_8mb.bin  # ESP32 S3
else
  esptool.py --chip $CHIP --port $AMPY_PORT erase_flash  # ESP32
fi

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
