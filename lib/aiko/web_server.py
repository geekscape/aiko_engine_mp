# lib/aiko/web_server.py: version: 2020-10-11 05:00
#
# Usage
# ~~~~~
# import aiko.web_server as web_server
# web_server.initialise()
#
# To Do
# ~~~~~
# - None, yet !

import network
import socket

def web_server():
  print("  ###### Web:  web_server()")
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(("", 80))
  sock.listen(0)

  while True:
    connection, address = sock.accept()
    print("  ###### Web:  Connection: " + str(address))
    request = connection.recv(1024).decode()
    print("  ###### Web:  Request: " + request)

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
        if key == "ssid": ssid = value
        if key == "password": password = value
      response = "<html><body>{}={}</body></html>".format(ssid, password)

    connection.send('HTTP/1.1 200 OK\n')
    connection.send('Content-Type: text/html\n')
    connection.send('Connection: close\n\n')
    connection.sendall(response)
    connection.close()

  sock.close()
  wifi = []
  return wifi

def wifi_configure(wifi):
  print("  ###### WiFi: wifi_configure()")
  ap = network.WLAN(network.AP_IF)
  ap.config(essid="swagbadge")
  ap.config(max_clients=1)
  ap.active(True)
  wifi = web_server()
  ap.active(False)
  return wifi
