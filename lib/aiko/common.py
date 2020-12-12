# lib/aiko/common.py: version: 2020-12-06 16:00
#
# To Do
# ~~~~~
# - Improve set_handler() mechanism to not require individual handler shims

import machine
import os

AIKO_VERSION = "v03"

handlers = {}

def hostname():
  return os.uname()[0] + "_" + unique_id()

def log(message):
  handlers["log"](message)

def set_handler(name, handler):
  handlers[name] = handler

def unique_id():
  id = machine.unique_id()  # 6 bytes
  id = "".join(hex(digit)[-2:] for digit in id)
  return id  # 12 hexadecimal digits
