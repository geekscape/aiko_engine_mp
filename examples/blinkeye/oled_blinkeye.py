# examples/blinkeye/oled_blinkeye.py: version: 2020-11-25 04:00
#
# Display PBM 1-bit images on OLED
#
# Usage
# ~~~~~
# Use exmaples/blinkeye/install.sh
# Boot with both touch pads down to stop aiko from interfering
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> from examples.blinkeye.oled_blinkeye import run; run()
# 
#

import machine
import aiko.oled as oled
import time
oled.initialise()
oled0 = oled.oleds[0]
oled1 = oled.oleds[1]

IMG="examples/blinkeye/"

def run():
    # get a few extra fps, at 240Mhz, I get 14FPS for both screens (or 28fps per screen)
    machine.freq(240000000)
    oled0.invert(1)
    oled1.invert(1)

    # Original animated gif had lots of frames that were
    # identical, or very close. We skip loading dupes but
    # we push an identical frame to keep the correct timing
    imagesL = [
        oled.load_image(IMG + "L00.pbm"),
        0, # 01
        0, # 02
        oled.load_image(IMG + "L03.pbm"),
        0, # 04
        oled.load_image(IMG + "L05.pbm"),
        oled.load_image(IMG + "L06.pbm"),
        oled.load_image(IMG + "L07.pbm"),
        oled.load_image(IMG + "L08.pbm"),
        oled.load_image(IMG + "L09.pbm"),
        0, # 10
        oled.load_image(IMG + "L11.pbm"),
        oled.load_image(IMG + "L12.pbm"),
        0, # 13
        0, # 14
        0, # 15
        0, # 16
        0, # 17
        0, # 18
        0, # 19
        0, # 20
        0, # 21
        0, # 22
        0, # 23
        0, # 24
        0, # 25
        0, # 26
        0, # 27
        0, # 28
        0, # 29
        0, # 30
        0, # 31
        0, # 32
        0, # 33
        0, # 34
        0, # 35
        0, # 36
        0, # 37
        0, # 38
        0, # 39
        0, # 40
        0, # 41
        0, # 42
        0, # 43
        0, # 44
        0, # 45
        0, # 46
        0, # 47
        0, # 48
        0, # 49
        0, # 50
        0, # 51
        0, # 52
    ]
    imagesR = [
        oled.load_image(IMG + "R00.pbm"),
        0, # 01
        0, # 02
        oled.load_image(IMG + "R03.pbm"),
        0, # 04
        oled.load_image(IMG + "R05.pbm"),
        oled.load_image(IMG + "R06.pbm"),
        oled.load_image(IMG + "R07.pbm"),
        oled.load_image(IMG + "R08.pbm"),
        oled.load_image(IMG + "R09.pbm"),
        0, # 10
        oled.load_image(IMG + "R11.pbm"),
        oled.load_image(IMG + "R12.pbm"),
        0, # 13
        0, # 14
        0, # 15
        0, # 16
        0, # 17
        0, # 18
        0, # 19
        0, # 20
        0, # 21
        0, # 22
        oled.load_image(IMG + "R23.pbm"),
        oled.load_image(IMG + "R24.pbm"),
        0, # 25
        0, # 26
        0, # 27
        0, # 28
        0, # 29
        0, # 30
        0, # 31
        oled.load_image(IMG + "R32.pbm"),
        oled.load_image(IMG + "R33.pbm"),
        0, # 34
        0, # 35
        0, # 36
        0, # 37
        0, # 38
        0, # 39
        0, # 40
        0, # 41
        0, # 42
        0, # 43
        0, # 44
        0, # 45
        0, # 46
        0, # 47
        0, # 48
        0, # 49
        0, # 50
        0, # 51
        0, # 52
    ]

    timer = time.ticks_ms()
    cnt = 0
    while True:
        if (imagesL[cnt]): oled0.blit(imagesL[cnt], 0, 0) 
        if (imagesR[cnt]): oled1.blit(imagesR[cnt], 0, 0) 
        oled0.show()
        oled1.show()
        cnt+=1

        if cnt == 53:
            # 1000 for miliseconds, but remove 1/3 since cnt goes up 3 for 2 refreshes
            print(1000 * 53 / (time.ticks_ms() - timer), "fps")
            timer = time.ticks_ms()
            cnt = 0
