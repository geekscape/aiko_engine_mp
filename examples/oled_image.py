# examples/oled_image.py: version: 2020-11-24 04:00
#
# Display PBM 1-bit image on OLED
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/oled_image.py
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> import examples.oled_image as eg
# >>> from examples.oled_image import run
# >>> run()
#
# Notes
# ~~~~~
# - GIMP supports the PBM image format

import framebuf

import aiko.oled as oled
oled.initialise()
oled0 = oled.oleds[0]

IMAGE_FILENAME="examples/tux_64.pbm"

def load_image(filename):
    with open(filename, 'rb') as file:
        file.readline()  # magic number: P4
        file.readline()  # creator comment
        width, height = [int(value) for value in file.readline().split()]
        image = bytearray(file.read())
    return framebuf.FrameBuffer(image, width, height, framebuf.MONO_HLSB)

def run():
    buffer = load_image(IMAGE_FILENAME)
    oled0.invert(1)
    oled0.fill(1)
    oled0.blit(buffer, 0, 0)
    oled0.show()

    direction = 1
    while True:
        for i in range(64):
            oled0.scroll(direction, 0)
            oled0.show()
        direction = - direction
