# configuration/main.py: version: 2020-12-13 18:00 v03

settings = {
# "application":     "applications/default",  # Application to run
# "application":     "applications/joysticks",
# "application":     "applications/led_strip",
# "application":     "applications/nodebots",
# "application":     "applications/step_controller",
# "application":     "applications/squirrel",
  "application":     "applications/swagbadge",
# "application":     "lolibot",

  "denye_touch_pins": [12, 14],  # If touch_pins pressed, don't run "main.py"
  "gc_enabled":       False,     # Display Garbage Collector statistics
  "logger_enabled":   False,     # Display everyone's log output
  "oled_enabled":     True,      # OLED attached
  "services_enabled": False      # Use Aiko Services infrastructure
}

def parameter(name, settings=settings):
  if name in settings: return settings[name]
  return False
