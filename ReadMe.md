Aiko Engine MP ([microPython](http://micropython.org))
==============

Contents
--------
- [Overview](#overview)
- [Installation](#installation)
- [Resources](#resources)

Pages
-----
- [Contributors](Contributors.md)
- [Software license](License)

<a name="overview" />

Overview
--------
The Aiko Engine MP provides ...

- Modular [microPython](http://micropython.org) based framework
- Abstractions for event handling, networking and timers
- End user Wi-Fi configuration via a Wi-Fi Access Port and web server
- Application firmware OTA (Over The Air) upgrader
- Low-level LED panel graphics functions
- Multiple OLED screens
- Integrates MQTT and distributed services
- Supports [LCA2021 SwagBadge project](http://www.openhardwareconf.org/wiki/Swagbadge2021)
- Supports [LCA2018 LoliBot robotics project](https://github.com/CCHS-Melbourne/LoliBot)
- Supports [LCA2017 IoTuz project](http://www.openhardwareconf.org/wiki/OHC2017)
- Tested on a range of ESP32 development boards

<a name="installation" />

Installation
-------------

- Download the source code from <https://github.com/geekscape/aiko_engine_mp>
```
    git clone https://github.com/geekscape/aiko_engine_mp
    cd aiko_engine_mp
```
- Ensure you have a
  [compatible hardware board](https://github.com/micropython/micropython/wiki/Boards-Summary) or
  [compatible microPython port](https://github.com/micropython/micropython/tree/master/ports)
- Make sure you have a Python
  [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) set-up, including
  [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper)
- Create `mkvirtualenv micropython` and work on the new virtual environment
```
    workon micropython
```
- Install mpfshell
```
    pip install esptool
    pip install -U mpfshell
```
- Plug in your ESP32 device and make sure you can see it,
  e.g `ls /dev/tty.*` provides e.g `/dev/tty.wchserial1410`
- Export the serial port to an environment variable, so mpfshell can use it,
  e.g `export AMPY_PORT=<port>` where `port` is the device address shown
  by the `ls` command above
- Download latest [microPython](http://micropython.org/download)
- Flash microPython
```
    ./scripts/flash_micropython.sh
```
- Run the Aiko Engine MP flash script
```
    ./scripts/mpf_script.sh ./scripts/aiko.mpf
```

Note: For Lolin32-Lite boards, the serial port can be notoriously problematic
and requires a slight delay in order for the connection to occur properly.
If you're seeing errors that look like `Could not enter raw repl` then this is probably related.

For `mpfshell` (version v0.9.1 and earlier) on Mac OS X or Windows, this
problem may be fixed via this [patch](https://github.com/wendlers/mpfshell/commit/52b0636c82b06a07daa5731550f86b0d7ebc7608)

<a name="resources" />

Resources
---------
Associated open-source ESP32 hardware projects ...

- [OHMC team's](https://twitter.com/swagbadge2021) -
  [LCA2021 SwagBadge](http://www.openhardwareconf.org/wiki/Swagbadge2021)
- [John Spencer's](https://twitter.com/mage0r) -
  [LCA2018 LoliBot robot](https://github.com/CCHS-Melbourne/LoliBot)
- [OHMC team's](http://www.openhardwareconf.org) -
  [LCA2017 IoTuz](http://www.openhardwareconf.org/wiki/OHC2017)