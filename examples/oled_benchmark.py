# examples/oled_benchmark.py: version: 2020-11-25 04:00
#
# Display PBM 1-bit images on OLED
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/oled_benchmark.py
# mpfs [/]> put examples/tux_nice.pbm
# mpfs [/]> put examples/tux_zoom.pbm
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> from examples.oled_benchmark import run
# >>> run()
#

import machine
import aiko.oled as oled
import time
oled.initialise()
oled0 = oled.oleds[0]
oled1 = oled.oleds[1]

def run():
    images = [
        oled.load_image("examples/tux_nice.pbm"),
        oled.load_image("examples/tux_zoom.pbm")
    ]

    lastcnt = 0
    cnt = 0
    timer = time.ticks_ms()
    while True:
        oled0.blit(images[cnt % 2], 0, 0)
        cnt+=1
        oled0.show()
        machine.lightsleep(1)
        oled1.blit(images[cnt % 2], 0, 0)
        cnt+=2
        oled1.show()
        machine.lightsleep(1)

        if cnt % 99 == 0:
            # 1000 for miliseconds, but remove 1/3 since cnt goes up 3 for 2 refreshes
            print(666 * (cnt-lastcnt)/(time.ticks_ms() - timer), "fps")
            timer = time.ticks_ms()
            lastcnt = cnt
