# lib/aiko/upgrade.py: version: 2021-01-23 09:00 v05
#
# mosquitto_pub -t upgrade/aiko_00 -r  \
#     -m "(upgrade VERSION MANIFEST_URL MANIFEST_CHECKSUM MANIFEST_SIZE)"
#
# mosquitto_pub -h lounge.local -t upgrade/aiko_00 -r -m '(upgrade v05 http://209.141.52.199:8888/aiko_v05/manifest 60371cc473d0aa7c0cbefbc760c30665 1585)'
#
# mosquitto_sub -t upgrade/aiko_00 -v
#
# To Do
# ~~~~~
# - Improve upgrade mechanism to use "import sys; sys.path" !

import gc
import os
from threading import Thread

import aiko.common as common
import aiko.event
import aiko.oled as oled
import aiko.web_client
import shutil

import configuration.mqtt

file_count = None
in_progress = False
manifest_checksum = None
manifest_size = None
manifest_url = None
version = None

def get_version():
  return version

def upgrade_handler():
  global in_progress, version

  if version and not in_progress:
    in_progress = True
    Thread(target=upgrade_thread).start()

def upgrade_thread():
  global in_progress
  global file_count, manifest_checksum, manifest_size, manifest_url, version
  try:
    common.log("Firmware upgrade start")
    gc.collect()

    manifest_pathname = "manifest"
    shutil.path_remove(manifest_pathname)
# TODO: Remove all "*_new" and "*_old"

    aiko.web_client.http_get_file(manifest_url, manifest_pathname)
# TODO: Verify "manifest_pathname" actual file size versus "manifest_size"
# TODO: Verify "manifest_pathname" checksum

    top_level_files = []
    url_prefix = manifest_url.rpartition("/")[0]
    with open(manifest_pathname, "r") as manifest_file:
      file_index = 0
      for line in manifest_file.readlines():
        file_index += 1
        file_checksum, file_size, filepath = line.split()
        url_suffix = filepath.partition("/")[-1]
        file_url = "/".join([url_prefix, url_suffix])

        pathname = url_suffix.partition("/")
        if not pathname[0] in top_level_files:
          top_level_files.append(pathname[0])
        pathname = "".join([pathname[0] + "_new"] + list(pathname[1:]))

        print(file_url + " --> " + pathname)
        common.log("Firmware get ... %d of %d" % (file_index, file_count))
        aiko.web_client.http_get_file(file_url, pathname)
# TODO: Verify actual file size versus size stated in the "manifest"
# TODO: Verify actual file checksum

    shutil.path_remove(manifest_pathname)
    shutil.file_copy("configuration/net.py",  "configuration_new/net.py")
    shutil.file_copy("configuration/keys.db", "configuration_new/keys.db")

    common.log("Firmware install")
    for file in top_level_files:
      try:
        print("Rename %s to %s" % (file + "_new", file))
        shutil.path_remove(file)
        os.rename(file + "_new", file)
      except OSError:
        print("OSError")

    common.log("Firmware upgrade success !")
    common.log("Please reboot :)")
  except Exception as exception:
    common.log("Firmware upgrade failed :(")
    import sys
    sys.print_exception(exception)
  finally:
    in_progress = False
    version = None

def on_upgrade_message(topic, payload_in):
  global file_count, manifest_checksum, manifest_size, manifest_url, version

  if payload_in.startswith("(upgrade "):
    tokens = payload_in[9:-1].split()
    if tokens[0] > common.AIKO_VERSION:
      version = tokens[0]
      manifest_url = tokens[1]
      manifest_checksum = tokens[2]
      manifest_size = int(tokens[3])
      file_count = int(tokens[4])
      common.annunicator_log_symbol = "F"
      oled.set_annunciator(common.ANNUNCIATOR_LOG, common.annunicator_log_symbol, True)
      common.log("Firmware upgrade available: " + version)
    return True

def initialise(settings=configuration.mqtt.settings):
  import aiko.mqtt
  upgrade_topic = settings["upgrade_topic"]
  aiko.mqtt.add_message_handler(on_upgrade_message, upgrade_topic)
