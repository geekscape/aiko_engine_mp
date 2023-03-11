# applications/stream_train.py: version: 2022-07-09 00:00 v00

import machine
from machine import Pin

import aiko.event as event

pin17 = None
pin22 = None

def handler():
#   global pin17, pin22

    pin22.value(pin17.value())

def initialise():
    global pin17, pin22

    pin16 = Pin(16, Pin.OUT)
    pin16.value(0)
    pin17 = Pin(17, Pin.IN, Pin.PULL_UP)
    pin22 = Pin(22, Pin.OUT)

    event.add_timer_handler(handler, 10)
