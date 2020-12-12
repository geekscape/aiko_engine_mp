# lib/aiko/upgrade.py: version: 2020-12-12 13:00
#
# mosquitto_pub -t aiko/upgrade -r  \
#     -m "(upgrade VERSION MANIFEST_URL MANIFEST_CHECKSUM MANIFEST_SIZE)"
#
# mosquitto_pub -h lounge.local -t aiko/upgrade -r -m '(upgrade v03 http://205.185.125.62:8888/aiko_v03/manifest 60371cc473d0aa7c0cbefbc760c30665 1585)'
#
# mosquitto_sub -t aiko/upgrade -v
#
# To Do
# ~~~~~
# - Replace "upgrade_handler()" with proper Aiko Engine button handler

import gc

import aiko.common as common
import aiko.event
import aiko.mqtt

import configuration.mqtt

manifest_checksum = None
manifest_size = None
manifest_url = None
version = None

def upgrade_handler():
  if common.touch_pins_check([12, 14]):
    common.log("Firmware upgrade start")

def on_upgrade_message(topic, payload_in):
  global version, upgrade_url, checksum

  if payload_in.startswith("(upgrade "):
    tokens = payload_in[9:-1].split()
    if tokens[0] > common.AIKO_VERSION:
      version = tokens[0]
      manifest_url = tokens[1]
      manifest_checksum = tokens[2]
      manifest_size = tokens[3]
      common.log("Firmware upgrade available: " + version)
    return True

def initialise(settings=configuration.mqtt.settings):
  upgrade_topic = settings["upgrade_topic"]
  aiko.mqtt.add_message_handler(on_upgrade_message, upgrade_topic)
  aiko.event.add_timer_handler(upgrade_handler, 5000)
