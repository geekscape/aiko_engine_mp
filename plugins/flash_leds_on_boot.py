# Flash configured LEDs on boot.

import aiko.led
import time
import binascii

DURATION_MS = 100
COLOURS = ["e40303", "ff8c00", "ffed00", "008026", "004dff", "750787"]
GAMMAS = [v for v in binascii.a2b_base64(b"".join([
  # Overkill, but I wanted the orange to look orange.
  # https://learn.adafruit.com/led-tricks-gamma-correction/the-quick-fix
  b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEBAQEBAQEBAQECAgICAgICAgMDA",
  b"wMDAwMEBAQEBAUFBQUGBgYGBwcHBwgICAkJCQoKCgsLCwwMDQ0NDg4PDxAQERESEhMTFB",
  b"QVFRYWFxgYGRkaGxscHR0eHyAgISIjIyQlJicnKCkqKywtLi8wMTIyMzQ2Nzg5Ojs8PT4",
  b"/QEJDREVGSElKS01OT1FSU1VWV1laXF1fYGJjZWZoaWttbnByc3V3eHp8fn+Bg4WHiYqM",
  b"jpCSlJaYmpyeoKKkp6mrra+xtLa4ur2/wcTGyMvN0NLV19rc3+Hk5+ns7/H09/n8/w=="
]))]

def gammify(colour):
  return tuple(GAMMAS[v] for v in colour)

def h2c(hex):
  return tuple(v for v in binascii.unhexlify(hex))

def initialise():
  colours = [aiko.led.black] + [gammify(h2c(hex)) for hex in COLOURS] + [aiko.led.black]
  ncolours = len(colours)
  npixels = aiko.led.np.n
  delay = max(1, DURATION_MS // (ncolours + npixels))

  aiko.led.fill(aiko.led.black)
  aiko.led.np.write()

  for offset in range(0 - ncolours, npixels):
    for index in range(ncolours):
      pixel = offset + index
      if 0 <= pixel < npixels:
        aiko.led.np[pixel] = colours[index]
    aiko.led.np.write()
    time.sleep_ms(delay)

  aiko.led.fill(aiko.led.black)
  aiko.led.np.write()
