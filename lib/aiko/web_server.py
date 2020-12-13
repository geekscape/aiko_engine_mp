# lib/aiko/web_server.py: version: 2020-12-13 18:30 v04
#
# Usage
# ~~~~~
# import aiko.web_server as web_server
# ssid_password = web_server.wifi_configure(wifi)
#
# To Do
# ~~~~~
# - "sock.unbind()" or "sock.close()" neither appears to work

import network
import socket

import aiko.common as common

sock = None
W = "### Web:  "
WIFI_AP_SSID = "aiko" + common.serial_id()

def web_server():
  global sock
# print(W + "web_server()")
  ssid = "unknown"
  password = "unknown"
  if not sock:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 80))
    sock.listen(0)

  waiting_for_post_request = True
  while waiting_for_post_request:
    connection, address = sock.accept()
#   print(W + "Connection: " + str(address))
    request = connection.recv(1024).decode()
#   print(W + "Request: " + request)

    if request.startswith("GET "):
      response = """<html><head><title>LCA2021 SwagBadge</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body><form method="POST">
            SSID:<input type="text" name="ssid"/><br/>
            Password:<input type="text" name="password"/><br/>
            <input type="submit"/>
        </form></body>
      </html>"""

    if request.startswith("POST "):
      request = request.splitlines()[-1].split("&")
      ssid = password = ""
      for item in request:
        key, value = item.split("=")
        if key == "ssid": ssid = url_decode(value)
        if key == "password": password = url_decode(value)
      response = "<html><body>WiFi connecting to %s</body></html>" % ssid
      waiting_for_post_request = False

    try:
      connection.send('HTTP/1.1 200 OK\n')
      connection.send('Content-Type: text/html\n')
      connection.send('Connection: close\n\n')
      connection.sendall(response)
      connection.close()
    except Exception:
      print(W + "Failed when sending response")

# sock.close()
  return (ssid, password)

def url_decode(url_string):
  if not url_string:
    return ""

  url_string = url_string.replace("+", " ")
  tokens = url_string.split("%")

  if len(tokens) == 1:
    return url_string

  result = [tokens[0]]
  append = result.append

  for item in tokens[1:]:
    append(chr(int(item[:2], 16)))
    append(item[2:])

  return "".join(result)

def wifi_configure(wifi):
  print(W + "WiFi configuration using SSID: " + WIFI_AP_SSID)
  common.log("Configure WiFi: " + WIFI_AP_SSID)

  ap_if = network.WLAN(network.AP_IF)
  ap_if.active(True)
  ap_if.config(essid=WIFI_AP_SSID)
  ap_if.config(max_clients=1)
  ip_address = ap_if.ifconfig()[0]
  common.log("Try http://" + ip_address)
  ssid_password = web_server()
  ap_if.active(False)
  return ssid_password
