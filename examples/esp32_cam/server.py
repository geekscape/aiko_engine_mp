# import server
# hdr, con, cam = server.initialize()
# server.connect(hdr, con, cam)
#
# To Do
# ~~~~~
# - Replace abbreviations
# - camera.deinit()

import camera
import esp
import gc
import machine
import network
import socket
import time

LED_FLASH_PIN = 4
LED_STATUS_PIN = 33

def initialize():
    print("#### server.initialize()")

    hdr = {
# Live Stream URL: /live
        "stream": """HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=kaki5
Connection: keep-alive
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Expires: Thu, Jan 01 1970 00:00:00 GMT
Pragma: no-cache
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET
Access-Control-Allow-Headers: *""",
        "frame": """--kaki5
Content-Type: image/jpeg"""}
    UID = const("username")  # authentication username
    PWD = const("password")  # authentication password

    cam = camera.init()
    print("Camera ready ? ", cam)

    APS = {
        "CHANGE_SSID": "CHANGE_PASSWORD"  # UPDATE WITH YOUR WI-FI DETAILS
    }
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    ssid_found = False
    while not ssid_found:
        print("#### Wi-Fi scan()")
        aps = sta_if.scan()
        for ap in aps:
            ssid = ap[0].decode('utf-8')
            if ssid in APS:
                print(f"SSID: {ssid}")
                ssid_found = True
                password = APS[ssid]
                sta_if.connect(ssid, password)
                break
        if not ssid_found:
            time.sleep(1.0)

    con = ()
    for i in range(10):
        if sta_if.isconnected():
            con = sta_if.status()
            print("Wi-Fi connected: " + sta_if.ifconfig()[0])
            break
        else:
            print("Wi-Fi not ready. Wait...")
            time.sleep(2)
    else:
        print("Wi-Fi not ready")

    return hdr, con, cam

def connect(pin_led_status, hdr, con, cam):
    print("#### server.connect()")

    if con and cam:
        if cam:
        # E (18859) camera: Value error for PIXFORMAT. 1 to 9 only
            camera.pixformat(0)     # 0: JPEG
        #    1:96x96,      2:160x120,   3:176x144,    4:240x176,  5:240x240
        #    6:320x240,    7:400x296,   8:480x320,    9:640x480, 10:800x600
        #   11:1024x768,  12:1280x720, 13:1280x1024, 14:1600x1200
        #   15:1920x1080, 16:720x1280, 17:864x1536,  18:2048x1536
            camera.framesize(6)     # 320x240 @1.33 espect ratio
            camera.quality(11)      # 0 (high) ... 63 (low)
            camera.contrast(2)      # -2 .. 2
            camera.saturation(2)    # -2 .. 2
            camera.brightness(2)    # -2 .. 2
            camera.speffect(0)      # 0: Color, 2: Greyscale
            camera.whitebalance(0)  # 0: default, 1:sunny, 2:cloudy, 3:office, 4:home
            camera.aelevels(0)      # -2 .. 2    Automatic Exposure
            camera.aecvalue(0)      # 0 .. 1200  Automatic exposure control
            camera.agcgain(0)       # 0 .. 30    Automatic Gain Control

            camera.flip(False)      # vertical
            camera.mirror(False)    # horizontal

        if con:
            # TCP server
            port = 80
            addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _socket.bind(addr)
            _socket.listen(1)
            # _socket.settimeout(5.0)

            while True:
                cs, ca = _socket.accept()   # wait for client connect
                print("Request from:", ca)
                w = cs.recv(200) # blocking
                (_,uid,pwd) = w.decode().split("\r\n")[0].split()[1].split("/")
                if not (uid==UID and pwd==PWD):
                    print("Not authenticated")
                    cs.close()
                    continue

                cs.write(b"%s\r\n\r\n" % hdr["stream"])
                pic=camera.capture
                put=cs.write
                hr=hdr["frame"]
                while True:
                    pin_led_status.value(not pin_led_status.value())
                    time_start = time.ticks_ms()
                    try:
                        put(b"%s\r\n\r\n" % hr)
                        put(pic())
                        put(b"\r\n")  # send and flush the send buffer
                    except Exception as e:
                        print("TCP send error", e)
                        cs.close()
                        break
                    gc.collect()
                    print(f"Frame: {time.ticks_ms() - time_start} ms, mem: {gc.mem_free()}")
    else:
        if not con:
            print("WiFi not connected.")
        if not cam:
            print("Camera not ready.")
        else:
            camera.deinit()
        print("System not ready. Please restart")

    print("System aborted")

def run():
    pin_flash_led = machine.Pin(LED_FLASH_PIN, machine.Pin.OUT)
    pin_flash_led.value(False)
    pin_status_led = machine.Pin(LED_STATUS_PIN, machine.Pin.OUT)
    pin_status_led.value(False)

    hdr, con, cam = initialize()
    pin_flash_led.value(True)
    time.sleep(0.25)
    pin_flash_led.value(False)
    connect(pin_status_led, hdr, con, cam)
