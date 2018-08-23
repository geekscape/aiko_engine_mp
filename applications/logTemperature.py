import machine
import dht
import onewire
import ds18x20
import utime
import json
import aiko.event as event
#import aiko.mqtt as mqtt


topTempHumid = None
oneWires = None
oneWireDevices = None

def event_send_temp(): 
    payload = {}

    topTempHumid.measure()
    payload["topTemperature"] = topTempHumid.temperature()
    payload["topHumidity"] = topTempHumid.humidity()

    oneWires.convert_temp()
    utime.sleep_ms(750)
    payload["waterTemperature"] = oneWires.read_temp(oneWireDevices[0])

    payload_out = json.dumps(payload)

    print(payload_out)
    #try: 
        #mqtt.client.publish("out/a", payload_out)
    #except Exception:
    #    print("Failed To Publish")

def initialise():
    global topTempHumid, oneWires, oneWireDevices
    print("initialising Sensors")

    topTempHumid = dht.DHT22(machine.Pin(16)) #DHT22
    oneWires = ds18x20.DS18X20(onewire.OneWire(machine.Pin(17))) #onewire Probe
    oneWireDevices = oneWires.scan()

    event.add_event_handler(event_send_temp, 10000)