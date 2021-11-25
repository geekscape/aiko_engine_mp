# Automatically shakes newly woken badges using @enderboi's protocol

import aiko, binascii, machine, sys, time

my_shake_source = binascii.hexlify(machine.unique_id()).decode('ascii')
my_reply_topic = aiko.mqtt.get_topic_path("public") + "/in"
messages = []

def on_message(topic, payload_in):
  messages.append((topic, payload_in))
  if len(messages) > 5:
    messages.pop(0)
  if payload_in.startswith("(boot ") and payload_in.endswith(" swagbadge)"):
    # TODO use aiko.event instead
    time.sleep_ms(500)
    hostname = topic.split('/')[1]
    reply_topic = "/".join(["public", hostname, "0", "in"])
    if reply_topic != my_reply_topic:
      aiko.mqtt.client.publish(reply_topic, "(shake 230 {})".format(my_shake_source))
      aiko.mqtt.client.publish(my_reply_topic, "(oled:log shook {})".format(hostname))
  return False

def initialise():
  # TODO broadcast message to indicate badge can be shook
  # TODO shake only badges that broadcast that message
  aiko.mqtt.add_message_handler(on_message, "$all/out")
