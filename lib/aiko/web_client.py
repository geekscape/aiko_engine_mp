# lib/aiko/web_client.py: version: 2020-12-13 18:00 v03
#
# Usage
# ~~~~~
# import aiko.web_client, aiko.upgrade
# aiko.web_client.http_get_file(aiko.upgrade.upgrade_url, "manifest")
#
# To Do
# ~~~~~
# - None, yet.

import os
import socket

import shutil

def http_get_async(url):
  _, _, host, path = url.split("/", 3)
  if ":" in host:
    host, port = host.split(":")
  else:
    port = 80
  ip_address = socket.getaddrinfo(host, port)[0][-1]
  sock = socket.socket()
  sock.connect(ip_address)
  sock.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path,host), "utf8"))
  started = False
  header = b""
  headers = {}
  while True:
    data = sock.recv(1024)
    if data:
      body = data
      if not started and b"HTTP" in body:
        started = True
      buffer = header + body
      if not headers and not b"\r\n\r\n" in buffer:
        header += body
        continue
      if b"\r\n\r\n" in buffer:
        try:
          headers, body = buffer.split(b"\r\n\r\n")
        except ValueError:
          raise Exception("File contains CRLF: " + url)
      if body:
        yield body
    else:
      break
  sock.close()

def http_get_file(url, pathname):
  shutil.make_directories(pathname)
  with open(pathname, "w") as file:
    try:
      data = http_get_async(url)
      while True:
        file.write(data.send(None))
    except StopIteration:
      file.close()

def http_get_response(url):
  response = b""
  try:
    data = http_get_async(url)
    while True:
      response += data.send(None)
  except StopIteration:
    pass
  return str(response, "utf-8")
