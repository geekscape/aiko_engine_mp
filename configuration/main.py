# configuration/main.py: version: 2018-05-30 00:00

settings = {
  "application":     "aiko/demonstration",      # Application to run
# "application":     "applications/joysticks",
# "application":     "applications/nodebots",
# "application":     "lolibot",

  "gc_enabled":       False,  # Display Garbage Collector statistics
  "logger_enabled":   False,  # Display everyone's log output
  "oled_enabled":     False,  # OLED attached
  "services_enabled": False   # Use Aiko Services infrastructure
}

def parameter(name, settings=settings):
  if name in settings: return settings[name]
  return False
