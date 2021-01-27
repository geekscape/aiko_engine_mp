
from lib.aiko import led,oled
from machine import Pin, TouchPad
import aiko.event
import time
from threading import Thread


# from examples.badge_np import run; run()

# this is set by aiko/led.py and configured in configuration/led.py
#num_np = 46
#np = neopixel.NeoPixel(Pin(19), 46)

# Neopixel demo code (c) Adafruit, adapted to Aiko by Marc MERLIN
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)
 
 
def rainbow_cycle(wait, loopcnt):
    for j in range(loopcnt):
        for i in range(num_np):
            pixel_index = (i * 256 // num_np) + j
            led.pixel(wheel(pixel_index & 255), i)
        led.write()
        time.sleep(wait)

def color_chase(color, wait):
    for i in range(num_np):
        led.pixel(color, i, True)
        time.sleep(wait)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
num_np = 0
 
badge_np_init = False

# left tux has a red LED with 50Ohm resistor between
# GPIO 19 (used for WS2812). This shows the control commands
# by blinking the red led.
# left tux also has one green LED plugged into GPIO22 and GND
ledpin1=Pin(22, Pin.OUT)

# right tux has 2 low power green eye LEDs plugged into SDA
# green is important as red/yellow is too low voltage and
# would take too many amps, as well as damage the I2C signal
# right tux has a front and back copper plane that can be
# used as a touchpad. Front is GPIO33 and rear is GPIO32

# On my board, with my soldering and my fingers, I see this:
# 1) when I'm not touching anything pads, read about 135
# 2) after being touched, they rebound to 5xx and quickly go
#    back down to 135
# 3) touching the front nose gives about 50-80 depending on pressure
# 4) touching the front foot gives 20-50 depending on pressure and my finger
# 5) touching the back foot gives around 20-50 on tux_rear
tux_front = TouchPad(Pin(33))
tux_rear  = TouchPad(Pin(32))


left_tux_led = True
def left_tux_led():
    global left_tux_led
    if tux_front.read() < 100 or tux_rear.read() < 100:
        left_tux_led = True
    else:
        left_tux_led = not left_tux_led

last_title=""
title=""
def right_tux_touch():
    global title, last_title
    title=""
    if tux_front.read() < 100:
        print("Front tux touched")
        title = "Front Touch"
    if tux_rear.read()  < 100:
        print("Rear tux touched")
        if title:
            title = "Front+Rear Touch"
        else:
            title = "Rear Touch"
    if title != last_title:
        last_title = title
        print("DOESNT WORK: Changing title to", title)
        oled.set_title(title)
        oled.write_title()
        # setting this does not affect dim value seen by MQTT "(led:debug)". Why?
        led.set_dim(0.4)


# edit configuration/main.py "application":     "examples/badge_np"
def initialise():
    global badge_np_init
    print("Init badge_np")
    ledpin1.value(left_tux_led)
    # Does not work
    oled.set_title("Test Title")
    oled.write_title()
    led.initialise()
    aiko.event.add_timer_handler(left_tux_led, 300, immediate=False)
    aiko.event.add_timer_handler(right_tux_touch, 1000, immediate=False)
    badge_np_init = True
    # https://pymotw.com/2/threading/
    # https://realpython.com/intro-to-python-threading/
    Thread(target=run, args=(True, )).start()

def run(thread=False):
    if thread: print("Start badge_np thread")
    if not badge_np_init: initialise()

    global num_np
    num_np = led.length

    while True:
        print("loop1:",led.dim); led.print_dim()
        color_chase(BLACK, 0.01)
        print("loop2:",led.dim); led.print_dim()
        color_chase(RED, 0.01)
        color_chase(YELLOW, 0.01)
        color_chase(GREEN, 0.01)
        color_chase(CYAN, 0.01)
        color_chase(BLUE, 0.01)
        color_chase(PURPLE, 0.01)
     
        print("loop3:",led.dim); led.print_dim()
        rainbow_cycle(0.005, 200)  # rainbow cycle with 1ms delay per step

