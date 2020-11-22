# lib/aiko/mqtt.py: version: 2020-11-22 19:00
#
# Usage
# ~~~~~
# import aiko.mqtt as mqtt
# mqtt.initialise()  # runs background mqtt thread
# mqtt.add_message_handler(mqtt.on_exec_message, "$me/exec")   ### INSECURE ###
# while True:
#   mqtt.client.check_msg()
#
# To Do
# ~~~~~
# - Refactor into class to eliminate global variables
# - Parameter for enabling on_message() debug logging (set via MQTT message)

import machine
import os
from threading import Thread
from time import sleep_ms
from umqtt.simple import MQTTClient
import uselect

import aiko.event as event
import aiko.net as net

import configuration.mqtt

WAIT_MQTT_CONNECTED_PERIOD = 1000  # milliseconds
WAIT_MQTT_INCOMING_MESSAGE = 10000  # milliseconds
WAIT_WIFI_CONNECTED_PERIOD = 10000  # milliseconds

client = None
connected = False
keepalive = 10  # seconds
message_handlers = []
namespace = "public"
topic_path = None

M = "  ###### MQTT: "

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

def is_connected():
  global connected
  return connected

def on_message(topic, payload_in):
  topic = topic.decode()
  payload_in = payload_in.decode()

# if topic == topic_path + "/in" and payload_in == "(repl)":
#   file = open("repl", "w")
#   file.close()
#   machine.reset()

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
        print(M + "on_message(): " + str(exception))

def on_exec_message(topic, payload_in):  ### INSECURE ###
  try:
    exec(payload_in, configuration.globals, {})
  except Exception as exception:
    print(M + "exec(): " + str(exception))
  return True

def mqtt_ping_handler():
  global client
  try:
    if client: client.ping()
  except OSError:
    disconnect("mqtt_ping")

def mqtt_thread():
  global client
  while True:
#   print(M + "Wi-Fi connected check")
    if net.is_connected():
#     print(M + "connect()")
      connect()
      while is_connected():
        if client:
#         print(M + "poll()")
          poller = uselect.poll()
          poller.register(client.sock, uselect.POLLIN)
          result = poller.poll(WAIT_MQTT_INCOMING_MESSAGE)
          if result:
#           print(M + "wait_msg()")
            try:
              client.wait_msg()
            except Exception:
              break  # inner loop
        else:
          sleep_ms(WAIT_MQTT_CONNECTED_PERIOD)
      disconnect("mqtt_thread")
    sleep_ms(WAIT_WIFI_CONNECTED_PERIOD)

def connect(settings=configuration.mqtt.settings):
  global client, connected, keepalive, topic_path

  client_id = get_hostname()
  client = MQTTClient(client_id,
    settings["host"], settings["port"], keepalive=keepalive)

  client.set_callback(on_message)
  client.set_last_will(topic_path + "/state", "nil")
  try:
    client.connect()
    event.add_timer_handler(mqtt_ping_handler, keepalive * 1000)

    for topic in settings["topic_subscribe"]:
      if topic.startswith("$all/"): topic = "+/+/+" + topic[4:]
      if topic.startswith("$me/"): topic = topic_path + topic[3:]
      client.subscribe(topic)

    connected = True
    print(M + "Connected to %s: %s" % (settings["host"], topic_path))
  except Exception:
    disconnect("connect")

def disconnect(caller_name):
  global client, connected

  if client:
    print(M + "Disconnected by " + caller_name)
    connected = False
    event.remove_timer_handler(mqtt_ping_handler)
    try:
      client.disconnect()
    except Exception:
      pass
    client = None

def initialise(settings=configuration.mqtt.settings):
  global keepalive, topic_path

  keepalive = settings["keepalive"]
  topic_path = settings["topic_path"]
  if topic_path == "$me": topic_path = get_topic_path(namespace)
  if settings["mqtt_insecure_exec"]:
    add_message_handler(on_exec_message, "$me/exec")

  Thread(target=mqtt_thread).start()
