# configuration/boot.py: version: 2018-02-11 00:00

settings = {
  "gc_enabled":       False,  # Display Garbage Collector statistics
  "logger_enabled":   False,  # Display everyone's log output
  "lolibot_enabled":  False,  # LoliBot application
  "oled_enabled":     False,  # OLED attached
  "services_enabled": False   # Use Aiko Services infrastructure
}

def parameter(name, settings=settings):
  if name in settings: return settings[name]
  return False
