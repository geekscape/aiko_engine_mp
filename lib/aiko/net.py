# lib/aiko/net.py: version: 2018-02-11 00:00
#
# Usage
# ~~~~~
# import aiko.net as net
# net.initiqlise()
#
# To Do
# ~~~~~
# - Note 1: If all APs and SSIDs tried unsuccessfully, then retry Wi-Fi scan
# - Note 2: Time-out in case Wi-Fi API connection fails
#
# - If Wi-Fi station connnection fails, then become a Wi-Fi Access Point
#
# - If OLED configured, write network status message to OLED

import network

from threading import Thread
from time import sleep

import aiko.event as event
import aiko.led as led
import aiko.mqtt as mqtt

import configuration.net

led.locked = 1
led_color = led.red
led_counter = 0.0
led_delta = 0.02
led_max = 0.2

# Parameter(s)
#   wifi: List of tuples, each one containing the Wi-Fi AP SSID and password
#
# Returns boolean: Wi-Fi connected flag

def wifi_connect(wifi=configuration.net.wifi):
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  aps = sta_if.scan()

  for ap in aps:  # Note 1
    for ssid in wifi:
      if ssid[0].encode() in ap:
        print("  ###### Wi-Fi: Connecting to " + ssid[0])
        sta_if.connect(ssid[0], ssid[1])
#       print("  ###### Wi-Fi: Waiting")
        while sta_if.isconnected() == False: sleep(0.1)  # Note 2
        print("  ###### Wi-Fi: Connected to " + ssid[0])
        break  # inner loop
    if sta_if.isconnected(): break  # outer loop

  return sta_if.isconnected()

def net_led_handler():
  global led_counter
  led_counter += led_delta
  led_dim = led_max - abs(led_counter % (led_max * 2) - led_max)
  led.pixel0(tuple([int(element * led_dim) for element in led_color]))

def net_manager():
  global led_color
  parameter = configuration.main.parameter

  while not wifi_connect(): sleep(0.5)
  led_color = led.blue

  if parameter("services_enabled"):
    import aiko.services as services
    services.initialise()
  else:
    mqtt.initialise()
  led_color = led.green

  while True:
    mqtt.client.wait_msg()

def initialise():
  event.add_event_handler(net_led_handler, 100)
  net_thread = Thread(target=net_manager)
  net_thread.start()
