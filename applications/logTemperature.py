import machine
import dht
import onewire
import sgp30
import ds18x20
import utime
import json
import aiko.event as event
#import aiko.mqtt as mqtt

topTempHumid = None
oneWires = None
oneWireDevices = None
airMonitor = None

def event_send_temp(): 
    payload = {}

    topTempHumid.measure()
    payload["topTemperature"] = topTempHumid.temperature()
    payload["topHumidity"] = topTempHumid.humidity()

    oneWires.convert_temp()
    utime.sleep_ms(750)
    payload["waterTemperature"] = oneWires.read_temp(oneWireDevices[0])
    payload["co2eq"] = airMonitor.co2eq
    payload["tvoc"] = airMonitor.tvoc
    print("co2eq = %d ppm \t tvoc = %d ppb" % (payload["co2eq"], payload["tvoc"]))
    payload_out = json.dumps(payload)

    print(payload_out)
    utime.sleep_ms(250)

    #try: 
        #mqtt.client.publish("out/a", payload_out)
    #except Exception:
    #    print("Failed To Publish")

def initialise():
    global topTempHumid, oneWires, oneWireDevices, airMonitor
    print("initialising Sensors")

    topTempHumid = dht.DHT22(machine.Pin(16)) #DHT22
    oneWires = ds18x20.DS18X20(onewire.OneWire(machine.Pin(17))) #onewire Probe
    oneWireDevices = oneWires.scan()
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    airMonitor = sgp30.SGP30(i2c)

    print("SGP30 serial #", [hex(i) for i in sgp30.serial])
    
    airMonitor.iaq_init()
    airMonitor.set_iaq_baseline(0x8973, 0x8aae)

    event.add_event_handler(event_send_temp, 10000)