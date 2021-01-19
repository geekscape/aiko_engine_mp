# examples/buttons_sliders.py: version: 2020-10-17 04:00
#
# ESP32 Touch slider example
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
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/buttons_sliders.py
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> from examples.buttons_sliders import run
# >>> run()
#
# Notes
# ~~~~~
# touch = TouchPad(Pin(14))
# touch.config(500)  # threshold when pin is considered touched
# esp32.wake_on_touch(True)
# machine.lightsleep()  

import aiko.button
from aiko.common import map_value
import aiko.event
import aiko.oled

aiko.button.initialise(poll_rate=100)  # 10 Hz (default is 5 Hz)

def button_handler(pin_number, state):
    print("Button {}: {}".format(pin_number, "press" if state else "release"))

    screen = None
    if pin_number == 16: screen = aiko.oled.oleds[0]
    if pin_number == 17: screen = aiko.oled.oleds[1]

    if screen:
        screen.fill_rect(0, 16, 128, 8, 0)
        text = "Button {}: {}".format(pin_number, state)
        screen.text(text, 0, 16)
        screen.show()

def slider_handler(pin_number, state, value):
    print("Slider {}: {} {}".format(pin_number, state, value))

    screen = None
    if pin_number == 12: screen = aiko.oled.oleds[0]
    if pin_number == 14: screen = aiko.oled.oleds[1]

    if screen:
        screen.fill_rect(0, 32, 128, 8, 0)
        text = "Slider: {} {}".format(state, value)
        screen.text(text, 0, 32)
        if value:
            value = int(map_value(value, 0, 100, 0, 128))
            screen.fill_rect(0, 48, 128, 16, 0)
            screen.fill_rect(0, 48, value, 16, 1)
        screen.show()

def run():
    aiko.oled.oleds_clear(0)
    aiko.button.add_button_handler(button_handler, [16, 17])
#   aiko.button.add_touch_handler(button_handler, [12, 14, 15, 27])

    aiko.button.add_slider_handler(slider_handler, 12, 15)
    aiko.button.add_slider_handler(slider_handler, 14, 27)
