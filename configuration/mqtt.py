# configuration/mqtt.py: version: 2020-10-11 05:00

settings = {
# "host":            "mqtt.eclipse.org",
  "host":            "mqtt.fluux.io",
# "host":            "test.mosquitto.org",
  "keepalive":       60,
  "port":            1883,
  "topic_path":      "$me",
  "topic_subscribe": [ "$me/in", "$me/exec" ],
# "topic_subscribe": [ "$me/in", "$me/exec", "$all/log" ],

# Enable processing *INSECURE* exec() commands received via MQTT
  "mqtt_insecure_exec": False
}
