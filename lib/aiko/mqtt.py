# lib/aiko/mqtt.py: version: 2020-10-17 04:00
#
# Usage
# ~~~~~
# import aiko.mqtt as mqtt
# mqtt.initialise()
# mqtt.add_message_handler(mqtt.on_exec_message, "$me/exec")   ### INSECURE ###
# while True:
#   mqtt.client.check_msg()
#
# To Do
# ~~~~~
# - Parameter for enabling on_message() debug logging (set via MQTT message)
# - Only transmit "ping message" when no messages sent with "keepalive" time

import configuration.mqtt

import machine
import os

from umqtt.robust import MQTTClient

import aiko.event as event

client = None
keepalive = 60
message_handlers = []
namespace = "public"
topic_path = None

def add_message_handler(message_handler, topic_filter=None):
  message_handlers.append((message_handler, topic_filter))

def get_hostname():
  return os.uname()[0] + "_" + get_unique_id()

def get_topic_path(namespace):
  return namespace + "/" + get_hostname() + "/0"

def get_unique_id():
  id = machine.unique_id()  # 6 bytes
  id = "".join(hex(digit)[-2:] for digit in id)
  return id   # 12 hexadecimal digits

def on_message(topic, payload_in):
  topic = topic.decode()
  payload_in = payload_in.decode()

  if topic == topic_path + "/in" and payload_in == "(repl)":
    file = open("repl", "w")
    file.close()
    machine.reset()

  for message_handler in message_handlers:
    match = True
    filter = message_handler[1]
    if filter:
      if filter.startswith("$all/"): match = topic.endswith(filter[4:])
      if filter.startswith("$me/"):  match = topic == topic_path + filter[3:]
    if match:
      try:
        if message_handler[0](topic, payload_in): break
      except Exception as exception:
        print("  ###### MQTT: on_message(): " + str(exception))

def on_exec_message(topic, payload_in):  ### INSECURE ###
  try:
    exec(payload_in, configuration.globals, {})
  except Exception as exception:
    print("  ###### MQTT: exec(): " + str(exception))
  return True

def mqtt_ping_handler():
  if client: client.ping()

def initialise(settings=configuration.mqtt.settings):
  global client, keepalive, topic_path

  client_id = get_unique_id()
  keepalive = settings["keepalive"]
  topic_path = settings["topic_path"]
  if topic_path == "$me": topic_path = get_topic_path(namespace)

  client = MQTTClient(client_id,
    settings["host"], settings["port"], keepalive=keepalive)

  client.set_callback(on_message)
  client.set_last_will(topic_path + "/state", "nil")
  client.connect()  # TODO: Catch exception

  event.add_timer_handler(mqtt_ping_handler, keepalive * 1000)

  if settings["mqtt_insecure_exec"]:
    add_message_handler(on_exec_message, "$me/exec")

  for topic in settings["topic_subscribe"]:
    if topic.startswith("$all/"): topic = "+/+/+" + topic[4:]
    if topic.startswith("$me/"): topic = topic_path + topic[3:]
    client.subscribe(topic)

  print("  ###### MQTT: Connected to %s: %s" % (settings["host"], topic_path))
