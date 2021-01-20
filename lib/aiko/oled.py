# lib/aiko/oled.py: version: 2020-12-27 14:00 v05
#
# Usage
# ~~~~~
# import aiko.oled
# aiko.oled.initialise()
# oled.set_title("Title")
# oled.write_title()
# oled.log("Log message"))
#
# image = aiko.oled.load_image("examples/tux_nice.pbm")
# oled0 = aiko.oled.oleds[0]
# oled0.fill(0)
# oled0.blit(image, 32, 0)
# oled0.show()
#
# MQTT commands
# ~~~~~~~~~~~~~
# Topic: /in   (oled:clear)
#              (oled:log This is a test !)
#              (oled:pixel x y)
#              (oled:text x y This is a test !)
#              oled.bg=1; oled.fg=0
#
# Topic: /in   (oled:traits)
#        /out  (oled:traits ????)
#
# To Do
# ~~~~~
# - Use OLEDProxy.debug to see how often OLEDProxy.show() is called !
#
# - Determine whether the OLED screen can be refreshed faster than 10 FPS
# - Only register MQTT on_oled_message() if MQTT is enabled
# - Only register MQTT on_oled_log_message() if MQTT is enabled
# - Use https://github.com/guyc/py-gaugette/blob/master/gaugette/ssd1306.py
#
# Resources
# ~~~~~~~~~
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html

'''
ol = aiko.oled.oled
x = 0;  y = 32
bg = 1; fg = 0
ol.fill(bg)
ol.pixel(x, y, fg)
ol.text("text", x, y, fg)
ol.hline(x, y, w, fg)
ol.vline(x, y, h, fg)
ol.line(x1, y1, x2, y2, fg)
ol.rect(x, y, w, h, fg)
ol.fill_rect(x, y, w, h, fg)
ol.scroll(xs, ys)
ol.blit(frame_buffer, x, y, key)

ol.poweron()
ol.poweroff()
ol.invert(0|1)
ol.contrast(0 .. 255)
'''

import framebuf
from machine import Pin
import machine, ssd1306

import aiko.common as common

import configuration.oled

oleds = []
width = None
height = None
font_size = None
bottom_row = None
bg = 0
fg = 1

annunciators = "    "
log_annunciator = False
log_buffer = []
show_title = False
system_use_count = 0
title = ""

def initialise(settings=configuration.oled.settings):
  global show_title, width, height, font_size, bottom_row
  parameter = configuration.main.parameter

  Pin(int(settings["enable_pin"]), Pin.OUT).value(1)
  addresses = settings["addresses"]
  scl_pin = int(settings["scl_pin"])
  sda_pin = int(settings["sda_pin"])

  show_title = parameter("lock_title", settings)
  width = int(settings["width"])
  height = int(settings["height"])
  font_size = int(settings["font_size"])
  bottom_row = height - font_size

  i2c = machine.I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
# i2c.scan()
  for address in addresses:
    try:
      oled = ssd1306.SSD1306_I2C(width, height, i2c, addr=address)
      oleds.append(OLEDProxy(oled))
    except Exception:
      print("### OLED: Couldn't initialise device: " + hex(address))
  set_title("Aiko " + common.AIKO_VERSION)
  oleds_clear(bg)
  common.set_handler("log", log)

  import aiko.mqtt
  aiko.mqtt.add_message_handler(on_oled_message, "$me/in")
  if parameter("logger_enabled"):
    aiko.mqtt.add_message_handler(on_oled_log_message, "$all/log")

def oleds_enabled(enabled):
  for oled in oleds:
    oled.enabled = enabled

def oleds_system_use(system_use):
  global system_use_count
  if system_use:
    system_use_count += 1
    if system_use_count == 1:
      for oled in oleds: oled.store_enabled(True)
  else:
    system_use_count -= 1
    if system_use_count == 0:
      for oled in oleds: oled.restore_enabled()

def load_image(filename):
  with open(filename, 'rb') as file:
    file.readline()  # magic number: P4
    file.readline()  # creator comment
    width, height = [int(value) for value in file.readline().split()]
    image = bytearray(file.read())
  return framebuf.FrameBuffer(image, width, height, framebuf.MONO_HLSB)

def log(text):
  global log_annunciator
  log_buffer.append(text)
  if len(log_buffer) > 12:
    del log_buffer[0]
  if not log_annunciator:
    set_annunciator(common.ANNUNCIATOR_LOG, "L", True) 
    log_annunciator = True

def oleds_clear(color):
  for oled in oleds:
    oled.fill(color)
  oleds_show()

def oleds_log(text):
# common.lock(True)
  for oled in oleds:
    oled.scroll(0, -font_size)
    oled.fill_rect(0, bottom_row, width, font_size, bg)
  oleds_text(text, 0, bottom_row, fg)
  oleds_show()
# common.lock(False)

def oleds_show():
  if show_title: write_title()
  for oled in oleds:
    oled.show()

def oleds_text(text, x, y, color):
  index = 0
  while text and len(oleds) > index:
    oleds[index].text(text, x, y, color)
    index += 1
    text = text[16:]

def set_annunciator(position, annunciator, write=False):
  global annunciators
  annunciators = annunciators[:position]+ annunciator+ annunciators[position+1:]
  set_title(title)
  if write and oleds:
    oleds_system_use(True)
    oleds[0].fill_rect(font_size * 12, 0, font_size * 4, font_size, fg)
    oleds[0].text(annunciators, font_size * 12, 0, 0)
    oleds_show()
    oleds_system_use(False)

def set_title(title_):
  global title
  title = (title_ + ' '*12)[:12] + annunciators

def test(text="Line "):
  for oled in oleds:
    oled.fill(bg)
  for y in range(0, height, font_size):
    oleds_text(text + str(y), 0, y, fg)
  oleds_show()

def write_title():
  for oled in oleds:
    oled.fill_rect(0, 0, width, font_size, fg)
  oleds_text(title, 0, 0, bg)

def on_oled_message(topic, payload_in):
  if payload_in == "(oled:clear)":
    oleds_clear(bg)
    return True

  if payload_in.startswith("(oled:log "):
    log(payload_in[10:-1])
    return True

  if payload_in.startswith("(oled:pixel "):
    tokens = [int(token) for token in payload_in[12:-1].split()]
    for oled in oleds:
      oled.pixel(tokens[0], height - tokens[1] - 1, fg)
    oleds_show()
    return True

  # (oled:text x y message)
  if payload_in.startswith("(oled:text "):
    tokens = payload_in[11:-1].split()
    try:
      x = int(tokens[0])
      y = height - font_size - int(tokens[1])
      text = " ".join(tokens[2:])
      oleds_text(text, x, y, fg)
      oleds_show()
    except Exception:
      print("Error: Expected (oled.text x y message) where x and y are integers")
    return True

  return False

def on_oled_log_message(topic, payload_in):
  log(payload_in)
  return True

class OLEDProxy:
  def __init__(self, oled):
    self.oled = oled
    self.debug = False
    self.enabled = True
    self.enabled_saved = self.enabled

  def restore_enabled(self):
    self.enabled = self.enabled_saved

  def store_enabled(self, enabled):
    self.enabled_saved = self.enabled
    self.enabled = enabled

  def blit(self, *args):
    if self.enabled: self.oled.blit(*args)

  def constrast(self, constrast):
    if self.enabled: self.oled.constrast(constrast)

  def fill(self, c):
    if self.enabled: self.oled.fill(c)

  def fill_rect(self, x, y, w, h, c):
    if self.enabled: self.oled.fill_rect(x, y, w, h, c)

  def hline(self, x, y, w, c):
    if self.enabled: self.oled.hline(x, y, w, c)

  def invert(self, invert):
    if self.enabled: self.oled.invert(invert)

  def line(self, x1, y1, x2, y2, c):
    if self.enabled: self.oled.line(x1, y1, x2, y2, c)

  def pixel(self, *args):
    if len(args) == 2: return self.oled.pixel(*args)
    if self.enabled: self.oled.pixel(*args)

  def poweroff(self):
    if self.enabled: self.oled.poweroff()

  def poweron(self):
    if self.enabled: self.oled.poweron()

  def rect(self, x, y, w, h, c):
    if self.enabled: self.oled.rect(x, y, w, h, c)

  def scroll(self, xstep, ystep):
    if self.enabled: self.oled.scroll(xstep, ystep)

  def show(self):
#   if self.debug: print("OLEDProxy.show()")
    if self.enabled: self.oled.show()

  def text(self, s, x, y, c=1):
    if self.enabled: self.oled.text(s, x, y, c)

  def vline(self, x, y, h, c):
    if self.enabled: self.oled.vline(x, y, h, c)

'''
# cs   = Pin( 2, mode=Pin.OUT)
# rst  = Pin(15, mode=Pin.OUT)
# mosi = Pin(14, mode=Pin.OUT)
# miso = Pin(12, mode=Pin.IN)
# sck  = Pin(13, mode=Pin.OUT)
# spi  = machine.SPI(baudrate=100000, sck=sck, mosi=mosi, miso=miso)
# oled = ssd1306.SSD1306_SPI(128, 64, spi)

# sck  = machine.Pin(19, machine.Pin.OUT)
# mosi = machine.Pin(23, machine.Pin.IN)
# miso = machine.Pin(25, machine.Pin.OUT)
# pcs  = machine.Pin(26, machine.Pin.OUT)
# pdc  = machine.Pin(27, machine.Pin.OUT)
# prst = machine.Pin(18, machine.Pin.OUT)

# spi  = machine.SPI(1,baudrate=1000000, sck=sck, mosi=mosi, miso=miso)
# oled = ssd1306.SSD1306_SPI(128, 64, spi, pdc, prst, pcs)
'''
