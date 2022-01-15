# configuration/led.py: version: 2020-12-13 18:30 v04

settings = {    # LED panel or string
  "apa106":       False,  # IoTuz and LoliBot use APA106 RGB LEDs
# "dimension":    (1,),
#  "dimension":    (8,),   # Edge lit acrylic panel
  "dimension":    (46,),
# "dimension":    (8, 8),
# "dimension":    (32, 8),
# "dimension":    (32, 32),
# "neopixel_pin":  4,     # TinyPICO
  "neopixel_pin": 19,     # swagbadge SAO_1 bottom right viewed from front
# "neopixel_pin": 15,     # Wemos OLED
# "neopixel_pin": 23,     # IoTuz
  "zigzag":       False,  # For 2D panels
  "dim":          0.2,    # default dim to save batteries/power over USB
}
