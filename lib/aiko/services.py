# lib/aiko/services.py: version: 2020-12-27 14:00 v05
#
# Usage
# ~~~~~
# import aiko.services
# aiko.services.initialise()
# while True:
#   aiko.mqtt.client.wait_msg()
#
# To Do
# ~~~~~
# * Implement tags, in "configuration/services.py"
#
# - Bootstrap protocol should include version number
# - If bootstrap() timeout, then use default settings for namespace, host, port

import configuration.services

import machine
import network
from time import sleep_ms
import usocket

import aiko.common
import aiko.mqtt
import configuration.mqtt

protocol = None
socket = None
topic_in = None
topic_log = None
topic_out = None
topic_path = None
topic_service = None
topic_state = None
username = None

def bootstrap():
  sta_if = network.WLAN(network.STA_IF)
  ip_address = sta_if.ifconfig()[0]

  global socket
  if socket == None:
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    socket.bind((ip_address, 4154))
  request = b"boot? " + ip_address + " 4154"
  address = ("255.255.255.255", 4153)
  socket.sendto(request, address)

  socket.setblocking(False)
  counter = 5000
  tokens = [""]
  while tokens[0] != "boot":
    try:
      response, addr = socket.recvfrom(1024)
      tokens = response.decode("utf-8").split()
    except OSError:
      sleep_ms(1)
      counter -= 1
      if counter == 0:
        socket.sendto(request, address)
        counter = 5000
  return tokens[1], tokens[2], tokens[3]
#        MQTT host, MQTT port, Namespace

def get_configuration(settings):
  hostname = aiko.common.hostname()
  pid = settings["pid"]
  protocol = settings["protocol"]
  username = settings["username"]
  return hostname, pid, protocol, username

def on_services_message(topic, payload_in):
  if topic == topic_service:
    if payload_in != "nil":
      tokens = payload_in[1:-1].split()
      if tokens[0] == "topic":
        service_manager_topic = tokens[1] + "/in"
        payload_out  = "(add " + topic_path
        payload_out += " " + protocol + " " + username + " ())"
        aiko.mqtt.client.publish(service_manager_topic, payload_out)
    return True

def initialise(settings=configuration.services.settings):
  global protocol, username, topic_in, topic_log
  global topic_path, topic_out, topic_service, topic_state

  hostname, pid, protocol, username = get_configuration(settings)
  mqtt_host, mqtt_port, namespace = bootstrap()
  topic_path = namespace + "/" + hostname + "/" + str(pid)
  topic_in = topic_path + "/in"
  topic_log = topic_path + "/log"
  topic_out = topic_path + "/out"
  topic_service = namespace + "/manager/service"
  topic_state = topic_path + "/state"

  settings = configuration.mqtt.settings
  settings["host"] = mqtt_host
  settings["port"] = mqtt_port
  settings["topic_path"] = topic_path
  settings["topic_subscribe"].append(settings["topic_path"] + "/in")
  settings["topic_subscribe"].append(topic_service)
  aiko.mqtt.add_message_handler(on_services_message)
  aiko.mqtt.initialise(settings)
