# lib/aiko/upgrade.py: version: 2020-12-12 13:00
#
# mosquitto_pub -t aiko/upgrade -r -m "(upgrade v03 UPGRADE_URL CHECKSUM)"
#
# mosquitto_sub -t aiko/upgrade -v
#   (upgrade v03 http://205.185.125.62/aiko_mp/aiko_v03.tar 2107480008)
#
# To Do
# ~~~~~
# - None, yet.

import aiko.common as common
import aiko.mqtt

import configuration.mqtt

checksum = None
upgrade_url = None
version = None

def on_upgrade_message(topic, payload_in):
  global version, upgrade_url, checksum

  if payload_in.startswith("(upgrade "):
    tokens = payload_in[9:-1].split()
    if tokens[0] > common.AIKO_VERSION:
      version = tokens[0]
      upgrade_url = tokens[1]
      checksum = tokens[2]
      common.log("Firmware upgrade available: " + version)
    return True

def initialise(settings=configuration.mqtt.settings):
  upgrade_topic = settings["upgrade_topic"]
  aiko.mqtt.add_message_handler(on_upgrade_message, upgrade_topic)
