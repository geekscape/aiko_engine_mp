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
# >>> import examples.buttons_sliders as eg
# >>> from examples.buttons_sliders import run
# >>> run()
#
# Force console output
# >>> eg.oleds = []
# >>> eg.run()
#
# Notes
# ~~~~~
# touch = TouchPad(Pin(14))
# touch.config(500)  # threshold when pin is considered touched
# esp32.wake_on_touch(True)
# machine.lightsleep()  

from machine import Pin, TouchPad

import aiko.event as event
import aiko.oled as oled

touch3 = TouchPad(Pin(15))
touch5 = TouchPad(Pin(12))
touch6 = TouchPad(Pin(14))
touch7 = TouchPad(Pin(27))

oleds = oled.oleds

def map_value(v, a, b, c, d):
    w = (v - a) / (b - a) * (d - c) + c
    return int(w)

def touch_slider_handler():
    try:
      pad_left_top = touch3.read()
      pad_left_bottom = touch5.read()
      pad_right_top = touch7.read()
      pad_right_bottom = touch6.read()
      slider_left = pad_left_bottom - pad_left_top
      slider_right = pad_right_bottom - pad_right_top

      if len(oleds) > 0:
          oled0 = oleds[0]
          oled0.fill_rect(0, 32, 48, 8, 0)
          if pad_left_top < 200 or pad_left_bottom < 200:
              oled0.text(str(slider_left), 0, 32)  # 0 - 100
              slider_left = map_value(slider_left, -100, 100, 0, 128)
              oled0.fill_rect(0, 48, 128, 16, 0)
              oled0.fill_rect(0, 48, slider_left, 16, 1)
          oled0.show()

          oled1 = oleds[1]
          oled1.fill_rect(0, 32, 48, 8, 0)
          if pad_right_top < 200 or pad_right_bottom < 200:
              oled1.text(str(slider_right), 0, 32)  # 0 - 100
              slider_right = map_value(slider_right, -100, 100, 0, 128)
              oled1.fill_rect(0, 48, 128, 16, 0)
              oled1.fill_rect(0, 48, slider_right, 16, 1)
          oled1.show()
      else:
          print("Touch: " + str(slider_left), end="    \r")
    except ValueError:
      pass

def run(handler=touch_slider_handler, period=100):
    event.add_timer_handler(handler, period)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(handler)
