import machine
import MS5611
import time
import aiko.event as event


ms = None

def event_send_temp(): 
    temp, pres, atl = ms.read()
    print("Temp: " str(temp) + " Time: " + str(time.ticks_ms() / 1000))


def initialise():
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    ms = ms5611.MS5611(i2c)
    event.add_event_handler(event_send_temp, 1000)
    event.loop() 