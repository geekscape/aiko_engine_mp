import machine
import ms5611
import time
import aiko.event as event
import aiko.mqtt as mqtt
from time import sleep


ms = None

def event_send_temp(): 
    temp, pres, atl = ms.read()
    print("Temp: " + str(temp) + " Time: " + str(time.ticks_ms() / 1000))
    mqtt.client.publish("out/a", str(temp))


def initialise():
    global ms
    print("initialising")
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    ms = ms5611.MS5611(i2c)

    sleep(10)
    event.add_event_handler(event_send_temp, 10)
    event.loop() 