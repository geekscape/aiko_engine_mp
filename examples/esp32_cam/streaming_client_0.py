#!/usr/bin/env python3

import cv2
import time

def camera_stream():
    dropped = 0
    video = cv2.VideoCapture("http://192.168.0.105/username/password")

    while True:
    #   if not video.isOpened():
    #       print("Reconnect")
    #   print("Before video.read()")

        ret, frame = video.read() # get frame-by-frame
    #   print(video.isOpened(), ret)
        if frame is not None:
            if dropped > 0:
                dropped = 0
            cv2.imshow("ESP32-CAM",frame)
            if cv2.waitKey(20) & 0xff == ord("x"):  # Press "x" to eXit
                break
        else:
            dropped += 1
            if dropped > 100:
               print("Video server is down")
               break

    video.release()
    cv2.destroyAllWindows()

while True:
    camera_stream()
    time.sleep(1.0)
