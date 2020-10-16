# examples/hall_effect.py: version: 2020-10-17 04:00
#
# ESP32 Hall Effect (magnetic sensor) example
#
# http://docs.micropython.org/en/latest/library/esp32.html#esp32.hall_sensor
#
# Usage
# ~~~~~
# export AMPY_PORT=/dev/tty.wchusbserial1410  # Lolin32
# ./scripts/mpf.sh
# mpfs [/]> put examples/hall_effect.py
# mpfs [/]> repl
# MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
# Type "help()" for more information.
# >>> import examples.hall_effect as eg
# >>> eg.run()
#
# Force console output
# >>> eg.oleds = []
# >>> eg.run()

import esp32
import aiko.event as event
import aiko.oled as oled

oleds = oled.oleds

def map_value(v, a, b, c, d):
    w = (v - a) / (b - a) * (d - c) + c
    return int(w)

def hall_sensor_handler():
    value = esp32.hall_sensor()
    if len(oleds) > 0:
        oled1 = oleds[0]
        oled1.fill_rect(0, 32, 48, 8, 0)
        oled1.text(str(value), 0, 32)  # 50 - 1800
        if value < 0: value = -value
        value = map_value(value, 50, 150, 0, 128)
        oled1.fill_rect(0, 48, 128, 16, 0)
        oled1.fill_rect(0, 48, value, 16, 1)
        oled1.show()
    else:
        print("Hall sensor: " + str(value), end="    \r")

def run(handler=hall_sensor_handler, period=100):
    event.add_timer_handler(handler, period)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(handler)
