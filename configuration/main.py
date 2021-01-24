# configuration/main.py: version: 2021-01-22 18:00 v05

settings = {
# "application":     "applications/default",  # Application to run
# "application":     "applications/joysticks",
# "application":     "applications/led_strip",
# "application":     "applications/nodebots",
  "application":     "applications/schedule/schedule",
# "application":     "applications/step_controller",
# "application":     "applications/squirrel",
# "application":     "applications/swagbadge",
# "application":     "lolibot",

  "denye_pins":       [12, 14],  # If touch_pins pressed, don't run "main.py"
  "logger_enabled":   False,     # Display everyone's log output
  "oled_enabled":     True,      # OLED attached
  "services_enabled": False      # Use Aiko Services infrastructure
  "plugins_enabled":  False      # Autoload additional code from the 'plugins/' folder
}

def parameter(name, settings=settings):
  if name in settings: return settings[name]
  return False
