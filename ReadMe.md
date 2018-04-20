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
- Currently supported and tested on a range of ESP32 development boards
- Support for low-level LED panel graphics functions
- Support for OLED screens
- Support Lolibot robotics project

<a name="installation" />

Installation
-------------

- Download the source code from https://github.com/geekscape/aiko_engine_mp
  and cd into it:
  `git clone https://github.com/geekscape/aiko_engine_mp && cd aiko_engine_mp`
- Ensure you have a
  [compatible board](https://github.com/micropython/micropython/wiki/Boards-Summary) or
  [compatible port](https://github.com/micropython/micropython/tree/master/ports)
- Make sure you have a Python 2
  [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) set-up, including
  [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper)
- Create `mkvirtualenv upython` and work on the new virtual environment
  `workon upython`
- Install AMPY from Adafruit `pip install -U adafruit-ampy`
- Install `esptool.py` `pip install -U esptool`
- Plug in your ESP32 device and make sure you can see it,
  e.g `ls /dev/tty.*` provides e.g `/dev/tty.wchserial1410`
- Export the serial port to an environment variable, so AMPY can use it,
  e.g `export AMPY_PORT=<port>` where `port` is the device address shown
  by the `ls` command above
- Run the Aiko Engine MP flash script, i.e `./scripts/flash_standard.sh`

Note: For Lolin32-Lite boards, the serial port is notoriously problematic
and requires a slight delay in order for the connection to occur properly.
If you're seeing errors that look like
`ampy.pyboard.PyboardError: could not enter raw repl`
then this is probably related.

In this case, set a delay to sleep the program when it iss uploading the files:
`export AMPY_DELAY=4` will usually do the trick.

<a name="resources" />

Resources
---------
Associated open-source ESP32 hardware ...

- [John Spencer's](https://twitter.com/mage0r)
  [LoliBot robot](https://github.com/mage0r/ESPkit-0://github.com/CCHS-Melbourne/LoliBot)
