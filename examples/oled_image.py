# examples/oled_image.py: version: 2020-11-25 04:00
#
# Display PBM 1-bit images on OLED
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/oled_image.py
# mpfs [/]> put examples/tux_64.pbm
# mpfs [/]> put examples/tux_nice.pbm
# mpfs [/]> put examples/tux_zoom.pbm
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
oled1 = oled.oleds[1]

def load_image(filename):
    with open(filename, 'rb') as file:
        file.readline()  # magic number: P4
        file.readline()  # creator comment
        width, height = [int(value) for value in file.readline().split()]
        image = bytearray(file.read())
    return framebuf.FrameBuffer(image, width, height, framebuf.MONO_HLSB)

def run():
    for oledx in oled.oleds:
        oledx.invert(1)
        oledx.fill(1)

    tux_64 = load_image("examples/tux_64.pbm")
    oled0.blit(tux_64, 0, 0)
    oled0.show()

    images = [
        load_image("examples/tux_nice.pbm"),
        load_image("examples/tux_zoom.pbm")
    ]

    direction = 1
    index = 0
    while True:
        oled1.blit(images[index], 0, 0)
        oled1.show()
        index = 1 - index  # 0 --> 1 --> 0 ...

        for i in range(64):
            oled0.scroll(direction, 0)
            oled0.show()
            oled1.scroll(- direction, 0)
            oled1.show()
        direction = - direction  # 1 --> -1 --> 1 ...
