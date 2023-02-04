# configuration/mqtt.py: version: 2023-02-04 07:00 v06

lca_schedule_topic = "public/lca/schedule/#"
upgrade_topic = "upgrade/aiko_00"

settings = {
  "host":            "geekscape.freeddns.org",  # SwagBadge server
# "host":            "mqtt.eclipse.org",
# "host":            "mqtt.fluux.io",
# "host":            "test.mosquitto.org",
  "keepalive":       60,
  "port":            1883,
  "topic_path":      "$me",
# "topic_subscribe": ["$me/in", "$me/exec", upgrade_topic],
# "topic_subscribe": ["$me/in", "$me/exec", upgrade_topic, "$all/log"],
  "topic_subscribe": ["$me/in", "$me/exec", lca_schedule_topic, upgrade_topic],
  "lca_schedule_topic": lca_schedule_topic,
  "upgrade_topic":   upgrade_topic,

# Enable processing *INSECURE* exec() commands received via MQTT
  "mqtt_insecure_exec": False
}
