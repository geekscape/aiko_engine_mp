# configuration/mqtt.py: version: 2018-02-11 00:00

settings = {
#  "host":            "iot.eclipse.org",
# "host":            "test.mosquitto.org",
  "host":            "192.168.0.110",
  "keepalive":       60,
  "port":            1883,
  "topic_path":      "$me",
  "topic_subscribe": [ "$me/exec", "$me/in", "$all/log" ],

# Enable processing *INSECURE* exec() commands received via MQTT
  "mqtt_insecure_exec": False
}
