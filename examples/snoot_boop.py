# examples/snoot_boop.py: version: 2020-11-23 04:00
#
# ESP32 Tux SAO Snoot boop (touch button)
#
# Description
# ~~~~~~~~~~~
# Simple #swagbadge touch button example.
# While these instructions are specifically for the Tux SAO PCB,
# this will work for any electically conductive material attached
# to any of the ESP32 touch sensitive GPIO pins.
#
# Hardware instructions
# ~~~~~~~~~~~~~~~~~~~~~
# - Solder 3x2 male header pins onto the Tux SAO (Simple Add On) PCB
# - On the Tux SAO PCB, carefully make a solder bridge between the
#   IO32 hole (Touch 9) and the gold pad immediately to the right of
#   that IO32 hole
# - Take care not to short those IO32 and IO33 holes together
# - Connect Tux SAO to #swagbadge SAO_2 (the only SAO connector with touch)
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/snoot_boop.py
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> import examples.snoot_boop as eg
# >>> from examples.snoot_boop import run
# >>> run()
#
# Notes
# ~~~~~
# touch = TouchPad(Pin(32))
# touch.config(500)  # threshold when pin is considered touched
# esp32.wake_on_touch(True)
# machine.lightsleep()  
#
# microPython Capacitive Touch
# https://docs.micropython.org/en/latest/esp32/quickref.html#capacitive-touch
# https://github.com/micropython/micropython/blob/master/ports/esp32/machine_touchpad.c
#
# Espressif:  ESP32 Touch Sensor Application Note
# https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md
#
# Nick Moore: ESP32 Capacitive Sensors (microPython)
# https://nick.zoic.org/art/esp32-capacitive-sensors
#
# Capacitive Touch Sensor, Berkeley IoT49 course (microPython)
# https://people.eecs.berkeley.edu/~boser/courses/49_sp_2019/L3_3_touch.html

import machine
from machine import Pin, TouchPad

import aiko.event as event
import aiko.oled as oled

led0 = Pin(19, machine.Pin.OUT, machine.Pin.PULL_UP)
led0.value(True)
led1 = Pin(22, machine.Pin.OUT, machine.Pin.PULL_UP)
led1.value(False)

oleds = oled.oleds
touch9 = TouchPad(Pin(32))

def map_value(v, a, b, c, d):
    w = (v - a) / (b - a) * (d - c) + c
    return int(w)

def snoot_boop_handler():
    try:
        value = touch9.read()

        oled0 = oleds[0]
        if value < 300:
            led0.value(not(led0.value()))
            led1.value(not(led1.value()))
            oled0.text("SNOOT", 40, 32)
            oled0.text("BOOP ", 40, 48)
        else:
            oled0.fill_rect(0, 32, 128, 64, 0)
        oled0.show()

        oled1 = oleds[1]
        oled1.fill_rect(0, 32, 48, 8, 0)
        oled1.text(str(value), 0, 32)  # 0 - 500
        value = map_value(value, 0, 500, 0, 128)
        oled1.fill_rect(0, 48, 128, 16, 0)
        oled1.fill_rect(0, 48, value, 16, 1)
        oled1.show()
    except ValueError:
        pass

def run(handler=snoot_boop_handler, period=100):
    event.add_timer_handler(handler, period)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(handler)
