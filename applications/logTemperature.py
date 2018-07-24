import machine
import ms5611
import time
import aiko.event as event
import aiko.mqtt as mqtt
from time import sleep


ms = None

def event_send_temp(): 
    temp, pres, atl = ms.read()
    
    try: 
        mqtt.client.publish("out/a", str(temp))
        result = "Okay"
    except Exception:
        result = "Fail"
    print(result + ": Temp: " + str(temp) + " Time: " + str(time.ticks_ms() / 1000))

def initialise():
    global ms
    print("initialising")
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    ms = ms5611.MS5611(i2c)

    event.add_event_handler(event_send_temp, 10000)