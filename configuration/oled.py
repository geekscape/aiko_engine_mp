# configuration/oled.py: version: 2020-12-13 18:30 v04
#
# SwagBadge OLED: ADDRESS = [0x3c, 0x3d], SCL= 4, SDA= 5
# Wemos     OLED: SCL= 4, SDA= 5, e.g large TTGO OLED
# TTGO      OLED: SCL=15, SDA= 4, e.g small TTGO OLED
# TinyPICO  OLED: SCL=22, SDA=21

settings = {
# "addresses":  [0x3c],
  "addresses":  [0x3c, 0x3d],  # SwagBadge
  "lock_title": True,
# "scl_pin":      15,          # Small TTGO
# "sda_pin":       4,
  "scl_pin":       4,          # Large TTGO, SwagBadge
  "sda_pin":       5,
# "scl_pin":      22,          # TinyPICO
# "sda_pin":      21,
  "enable_pin":   16,
  "width":       128,
  "height":       64,
  "font_size":     8
}
