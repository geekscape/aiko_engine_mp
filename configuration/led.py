# configuration/led.py: version: 2020-12-13 18:00 v03

settings = {    # LED panel or string
  "apa106":       False,  # IoTuz and LoliBot use APA106 RGB LEDs
# "dimension":    (1,),
  "dimension":    (8,),   # Edge lit acrylic panel
# "dimension":    (8, 8),
# "dimension":    (32, 8),
# "dimension":    (32, 32),
# "neopixel_pin":  4,     # TinyPICO
  "neopixel_pin": 13,     # Usually
# "neopixel_pin": 15,     # Wemos OLED
# "neopixel_pin": 23,     # IoTuz
  "zigzag":       False   # For 2D panels
}
