# lib/aiko/net.py: version: 2020-12-27 14:00 v05
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

import aiko.common as common
import aiko.event
import aiko.led as led
import aiko.web_server

import configuration.net

WIFI_CONNECTING_CLIENT_PERIOD = 500  # milliseconds
WIFI_CONNECTED_CHECK_PERIOD = 1000   # milliseconds
WIFI_CONNECTED_CLIENT_PERIOD = 5000  # milliseconds
WIFI_CONNECTING_RETRY_LIMIT = 20
WIFI_CONNECT_RETRY_LIMIT = 2

connected = False
wifi_configuration_updated = False

led.locked = 1
led_color = led.red
led_counter = 0.0
led_delta = 0.02
led_max = 0.2

W = "### WiFi: "

def is_connected():
  global connected
  return connected

# Parameter(s)
#   wifi: List of tuples, each one containing the Wi-Fi AP SSID and password
#
# Returns sta_if: Wi-Fi Station reference

def wifi_connect(wifi):
  global connected
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  common.log("WiFi scan")
  aps = sta_if.scan()

  for ap in aps:  # Note 1
    for ssid in wifi:
      if ssid[0].encode() in ap:
        print(W + "Connecting: " +  ssid[0])
        common.log("WiFi connecting:" +  ssid[0])
        sta_if.connect(ssid[0], ssid[1])
        for retry in range(WIFI_CONNECTING_RETRY_LIMIT):
          if sta_if.isconnected():
            print(W + "Connected: " + ssid[0])
            common.log("WiFi connected: " + ssid[0])
            connected = True
            wifi_configuration_update(wifi)
            break   # for retry
#         print(W + "Waiting")
          sleep_ms(WIFI_CONNECTING_CLIENT_PERIOD)
        if sta_if.isconnected(): break  # for ssid
        print(W + "Timeout: Bad password ?")
        common.log("Timeout:        Bad password ?")
    if sta_if.isconnected(): break  # for ap
  return sta_if

def wifi_configuration_update(wifi):
  global wifi_configuration_updated

  if wifi_configuration_updated:
    file = open("configuration/net.py", "w")
    file.write("wifi = [\n")
    for ssid_password in wifi:
      record = '  ("' + ssid_password[0] + '", "' + ssid_password[1] + '"),\n'
      file.write(record)
    file.write("]")
    file.close()
    print(W + "Configuration updated")
    common.log("WiFi configuration updated")
  wifi_configuration_updated = False

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
  global led_color, wifi_configuration_updated

  wifi = configuration.net.wifi
  while True:
    led_color = led.red
    if len(wifi):
      print(W + "Checking WiFi configuration with available networks")
      for retry in range(WIFI_CONNECT_RETRY_LIMIT):
        sta_if = wifi_connect(wifi)
        if sta_if.isconnected(): break
        sleep_ms(WIFI_CONNECTED_CHECK_PERIOD)
      while sta_if.isconnected():
        led_color = led.blue
        sleep_ms(WIFI_CONNECTED_CLIENT_PERIOD)
      wifi_disconnect(sta_if)
    ssid_password = aiko.web_server.wifi_configure(wifi)
    if len(ssid_password[0]):
      wifi.insert(0, ssid_password)
      wifi_configuration_updated = True

def initialise():
  aiko.event.add_timer_handler(net_led_handler, 100)
  Thread(target=net_thread).start()

  parameter = configuration.main.parameter
  if parameter("services_enabled"):
    import aiko.services as services
    services.initialise()
  else:
    import aiko.mqtt
    aiko.mqtt.initialise()
