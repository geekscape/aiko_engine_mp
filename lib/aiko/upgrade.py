# lib/aiko/upgrade.py: version: 2020-12-13 14:00
#
# mosquitto_pub -t upgrade/aiko -r  \
#     -m "(upgrade VERSION MANIFEST_URL MANIFEST_CHECKSUM MANIFEST_SIZE)"
#
# mosquitto_pub -h lounge.local -t upgrade/aiko -r -m '(upgrade v03 http://205.185.125.62:8888/aiko_v03/manifest 60371cc473d0aa7c0cbefbc760c30665 1585)'
#
# mosquitto_sub -t upgrade/aiko -v
#
# To Do
# ~~~~~
# - Replace "upgrade_handler()" with proper Aiko Engine button handler

import gc
from threading import Thread

import aiko.common as common
import aiko.event
import aiko.mqtt
import aiko.web_client
import shutil

import configuration.mqtt

in_progress = False
manifest_checksum = None
manifest_size = None
manifest_url = None
version = None

def upgrade_handler():
  global in_progress, version

  if common.touch_pins_check([12, 14]):
    if version and not in_progress:
      in_progress = True
      Thread(target=upgrade_thread).start()

def upgrade_thread():
  global in_progress, manifest_checksum, manifest_size, manifest_url, version
  try:
    common.log("Firmware upgrade start")
    gc.collect()
    _, _, host, manifest_pathname = manifest_url.split("/", 3)
    upgrade_directory, _ = manifest_pathname.split("/", 1)
    shutil.path_remove(upgrade_directory)
    aiko.web_client.http_get_file(manifest_url, manifest_pathname)
#   Verify "manifest_pathname" actual file size versus "manifest_size"

    url_prefix = manifest_url.rpartition("/")[0]
    with open(manifest_pathname, "r") as manifest_file:
      for record in manifest_file.readlines():
        file_checksum, file_size, filepath = record.split()
        url_suffix = filepath.partition("/")[-1]
        file_url = "/".join([url_prefix, url_suffix])
        pathname = "/".join([upgrade_directory, url_suffix])
        print(file_url + " --> " + pathname)
        aiko.web_client.http_get_file(file_url, pathname)
#       Verify actual file size versus size stated in the "manifest"

#   Move old directories and main.py
#   Move new directories and main.py

#   shutil.path_remove(upgrade_directory)
    version = None
    common.log("Firmware upgrade success")
  except Exception as exception:
    common.log("Firmware upgrade failed")
    import sys
    sys.print_exception(exception)
  finally:
    in_progress = False

def on_upgrade_message(topic, payload_in):
  global manifest_checksum, manifest_size, manifest_url, version

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
