# examples/blinkeye/oled_blinkeye.py: version: 2020-11-25 04:00
#
# Display PBM 1-bit images on OLED
#
# Usage
# ~~~~~
# Use examples/blinkeye/install.sh
# Boot with both touch pads down to stop aiko from interfering
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> from examples.blinkeye.oled_blinkeye import run; run()
# 
#

from machine import Pin, TouchPad
import machine
import aiko.oled as oled
import time
oled.initialise()
oled0 = oled.oleds[0]
oled1 = oled.oleds[1]

IMG="examples/blinkeye/"
top_left = TouchPad(Pin(15))
bottom_left = TouchPad(Pin(12))
top_right = TouchPad(Pin(27))
bottom_right = TouchPad(Pin(14))
button_left = Pin(16, Pin.IN, Pin.PULL_UP)
button_right = Pin(17, Pin.IN, Pin.PULL_UP)

# return from -3 (top) to 3 (bottom) or -128 if no touch
def mapTouchpad(top, bottom):
    # on my board, I need to add this to get close to 0
    correction = 15
    if top+bottom > 450:  return -128  # no touch
    if top-bottom+correction < -150: return -3
    if top-bottom+correction < -100: return -2
    if top-bottom+correction <  -50: return -1
    if top-bottom+correction <    0: return  0
    if top-bottom+correction <   50: return  1
    if top-bottom+correction <  100: return  2
    return 3

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
    leftcnt = 0
    leftdelay = 0
    lastleft = 0
    rightcnt = 0
    rightdelay = 0
    lastright = 0
    cnt = 0
    while True:
        left =  mapTouchpad(top_left.read(),  bottom_left.read())
        right = mapTouchpad(top_right.read(), bottom_right.read())

        if left == -128:  
            leftcnt+=1
            if right == -128:
                # if no slider is pushed, sync both eyes
                rightcnt = leftcnt
        else:
            print("left:  ", left, ", previous left:", lastleft, ", leftdelay: ", leftdelay, ", leftcnt: ", leftcnt)
            # if 0, we pause and don't change the image
            if lastleft != left:
                lastleft = left
                leftdelay = 0
            if left != 0:
                if leftdelay == 0:
                    dir = abs(left)/left
                    if abs(left) == 3: leftdelay = 3
                    if abs(left) == 2: leftdelay = 6
                    if abs(left) == 1: leftdelay = 10
                    leftcnt += int(dir)
                else:
                    leftdelay-=1

        if (leftcnt < 0):  leftcnt = 52
        if (leftcnt > 52): leftcnt = 0
        if (imagesL[leftcnt]): oled0.blit(imagesL[leftcnt], 0, 0) 
        # API: http://docs.micropython.org/en/latest/library/framebuf.html
        oled0.fill_rect(112, 56, 16, 8, 0)
        oled0.text(str(leftcnt), 112, 56, 1);
        oled0.show()

        if right == -128:  
            rightcnt+=1
        else:
            print("right:  ", right, ", previous right:", lastright, ", rightdelay: ", rightdelay, ", rightcnt: ", rightcnt)
            # if 0, we pause and don't change the image
            if lastright != right:
                lastright = right
                rightdelay = 0
            if right != 0:
                if rightdelay == 0:
                    dir = abs(right)/right
                    if abs(right) == 3: rightdelay = 3
                    if abs(right) == 2: rightdelay = 6
                    if abs(right) == 1: rightdelay = 10
                    rightcnt += int(dir)
                else:
                    rightdelay-=1

        if (rightcnt < 0):  rightcnt = 52
        if (rightcnt > 52): rightcnt = 0
        if (imagesR[rightcnt]): oled1.blit(imagesR[rightcnt], 0, 0) 
        oled1.fill_rect(0, 56, 16, 8, 0)
        oled1.text(str(rightcnt), 0, 56, 1);
        oled1.show()

        cnt += 1
        if cnt == 100:
            # 1000 for miliseconds, but remove 1/3 since cnt goes up 3 for 2 refreshes
            print(1000 * 100 / (time.ticks_ms() - timer), "fps")
            timer = time.ticks_ms()
            cnt = 0


    #print("left:  ", top_left.read(), bottom_left.read(), top_left.read() - bottom_left.read())
    #print("right: ", top_right.read(), bottom_right.read(), top_right.read() - bottom_right.read())
