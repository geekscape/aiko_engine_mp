# configuration/main.py: version: 2023-02-04 07:00 v06

settings = {
# "application":     "applications/default",  # Application to run
# "application":     "applications/joysticks",
# "application":     "applications/led_strip",
# "application":     "applications/nodebots",
# "application":     "applications/schedule/schedule",
# "application":     "applications/step_controller",
# "application":     "applications/stream_train",
# "application":     "applications/stylophone",
# "application":     "applications/squirrel",
# "application":     "applications/swagbadge",
# "application":     "lolibot",

  "denye_pins":       [12, 14],  # If touch_pins pressed, don't run "main.py"
# "denye_pins":       [12, 13],  # If touch_pins pressed, don't run "main.py"
  "led_enabled":      False,     # WS2812B LEDs attached
  "logger_enabled":   False,     # Display everyone's log output
  "oled_enabled":     True,      # OLED attached
  "services_enabled": True       # Use Aiko Services infrastructure
}

def parameter(name, settings=settings):
  if name in settings: return settings[name]
  return False
