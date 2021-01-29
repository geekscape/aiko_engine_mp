# Plugins

## What's a plugin?

**Plugins aren't the same as applications.** In particular: we only want
to be running one application at a time. To get a little RFC2119, the
application MAY assume it has sole control of what's shown on the OLED
displays, and MAY assume any touch sensor or push buttons are for it to
handle. Eventually, their `initialise` function might get a matching
`uninitialise`, or we might get _very_ clever and remove their handlers
automatically.

Plugins, on the other hand, MUST co-operate with each other, MUST NOT
assume they control the displays or inputs, and SHOULD work together.
We'll eventually run into conflicts we can't resolve without being
able to disable specific plugins, but let's see how long we can last.

## How do I enable and disable plugins?

Set the parameter `plugin_xxx_disabled` to stop your badge automatically
calling `plugins.xxx.initialise()` at startup. You can set that in
`configuration/main.py`, and check it with the code:

```python
import configuration
configuration.main.parameter("plugins_enabled")
```

## How do I add plugins?

Add Python modules to the `plugins` directory. They MUST contain an
`initialise` function. They MUST NOT be named `initialise`, as that
would conflict with the plugin system's initialisation code.

You'll be able to see your plugins at the REPL:

```plain
MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
Type "help()" for more information.
>>> import plugins
>>> dir(plugins)
['__class__', '__name__', '__file__', '__path__', 'initialise', 'auto_shake', 'test2']
>>> plugins.auto_shake.messages
[('public/esp32_10521c5de548/0/out', '(boot v05 swagbadge)')]
>>> plugins.test2.tested
True
```
