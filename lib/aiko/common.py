# lib/aiko/common.py: version: 2020-12-06 16:00
#
# To Do
# ~~~~~
# - None, yet.

import machine
import os

AIKO_VERSION = "Aiko v02"

log_handler = None

def hostname():
  return os.uname()[0] + "_" + unique_id()

def log(message):
  global log_handler

  if log_handler:
    log_handler(message)

def set_log_handler(handler):
  global log_handler
  log_handler = handler

def unique_id():
  id = machine.unique_id()  # 6 bytes
  id = "".join(hex(digit)[-2:] for digit in id)
  return id  # 12 hexadecimal digits
