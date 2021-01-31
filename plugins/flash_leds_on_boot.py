# Flash configured LEDs on boot.
# Tested with 235X pixels on SAO_1, data to IO19, and configuration.led.settings =
# {'zigzag': False, 'dimension': (235,), 'apa106': False, 'neopixel_pin': 19}

import aiko.led
from binascii import unhexlify, b2a_base64
from gc import collect
from time import sleep_us, ticks_us, ticks_diff

DURATION_MS = 250
COLOURS = ["000000", "e40303", "ff8c00", "ffed00", "008026", "004dff", "750787", "000000"]
COMPENSATION_MEASUREMENTS = 5

def h2c(hex):
  return tuple(v for v in unhexlify(hex))

def measure_write_time_us(write):
  collect()
  before_us = ticks_us()
  for _ in range(0, COMPENSATION_MEASUREMENTS): write()
  return ticks_diff(ticks_us(), before_us) // COMPENSATION_MEASUREMENTS

def noop(): pass

def swipe(buf, cbuf, step, callback=noop):
  lcbuf = len(cbuf)
  lbuf = len(buf)
  for head in range(0 - lcbuf, lbuf, step):
    lt = 0 - min(0, head)
    rt = min(0, lbuf - (head + lcbuf))
    w = lcbuf - lt + rt
    buf[head + lt : head + lt + w] = cbuf[lt : lcbuf + rt]
    callback()

def make_cbuf(hex_colours, colour_width=1):
  ncolours = len(hex_colours)
  colours = [aiko.led.apply_dim(h2c(hex)) for hex in hex_colours]
  cbuf = bytearray(3 * ncolours * colour_width)
  for c in range(ncolours):
    colour = bytearray(colours[c])
    for s in range(colour_width):
      offset = (c * colour_width + s) * 3
      cbuf[offset:offset+3] = colour
  return memoryview(cbuf)

def initialise():
  ncolours = len(COLOURS)
  pixel = aiko.led.np
  write = aiko.led.np.write
  write_time_us = measure_write_time_us(write)
  colour_width = 1
  while write_time_us * (ncolours * colour_width + pixel.n) // colour_width > DURATION_MS * 1000:
    colour_width += 1
  cbuf = make_cbuf(COLOURS, colour_width)
  expected_steps = (len(cbuf) + len(pixel.buf) + 3) // (colour_width * 3)
  delay_us = max(0, DURATION_MS * 1000 // expected_steps - write_time_us)
  def callback():
    write()
    sleep_us(delay_us)
  collect()
  swipe(pixel.buf, cbuf, colour_width * 3, callback)
