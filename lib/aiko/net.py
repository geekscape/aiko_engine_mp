# lib/aiko/net.py: version: 2020-11-22 19:00
#
# Usage
# ~~~~~
# import aiko.net as net
# net.initialise()  # runs background network thread
#
# To Do
# ~~~~~
# - Refactor into class to eliminate global variables
#
# - Note 1: If all APs and SSIDs tried unsuccessfully, then retry Wi-Fi scan
# - Note 2: Time-out in case Wi-Fi API connection fails
#
# - If Wi-Fi station connnection fails, then become a Wi-Fi Access Point
#
# - If OLED configured, write network status message to OLED

import network
from threading import Thread
from time import sleep_ms

import aiko.event as event
# import aiko.led as led

import configuration.net

WIFI_CONNECTED_SHORT_PERIOD = 100  # milliseconds
WIFI_CONNECTED_LONG_PERIOD = 2000  # milliseconds

connected = False

# led.locked = 1
# led_color = led.red
led_counter = 0.0
led_delta = 0.02
led_max = 0.2

W = "  ###### WiFi: "

def is_connected():
  global connected
  return connected

# Parameter(s)
#   wifi: List of tuples, each one containing the Wi-Fi AP SSID and password
# Returns
#   sta_if: Wi-Fi Station reference

def wifi_connect(wifi=configuration.net.wifi):
  global connected
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  aps = sta_if.scan()

  for ap in aps:  # Note 1
    for ssid in wifi:
      if ssid[0].encode() in ap:
        print(W + "Connecting to " + ssid[0])
        sta_if.connect(ssid[0], ssid[1])
#       print(W + "Waiting")
        while sta_if.isconnected() == False:  # Note 2
          sleep_ms(WIFI_CONNECTED_SHORT_PERIOD)
        print(W + "Connected to " + ssid[0])
        connected = True
        break  # inner loop
    if sta_if.isconnected(): break  # outer loop
  return sta_if

def wifi_disconnect(sta_if):
  sta_if.disconnect()
  print(W + "Disconnected")
  connected = False

def net_led_handler():
  global led_counter
  led_counter += led_delta
  led_dim = led_max - abs(led_counter % (led_max * 2) - led_max)
  led.pixel0(tuple([int(element * led_dim) for element in led_color]))

def net_thread():
# global led_color
  while True:
#   led_color = led.red
    sta_if = wifi_connect()
    if sta_if.isconnected():
#     led_color = led.blue
      while sta_if.isconnected():
        sleep_ms(WIFI_CONNECTED_LONG_PERIOD)
      wifi_disconnect(sta_if)

def initialise():
# event.add_timer_handler(net_led_handler, 100)
  Thread(target=net_thread).start()

  parameter = configuration.main.parameter
  if parameter("services_enabled"):
    import aiko.services as services
    services.initialise()
  else:
    import aiko.mqtt as mqtt
    mqtt.initialise()
