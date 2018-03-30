Aiko Engine MP ([microPython](http://micropython.org))
==============

Contents
--------
- [Overview](#overview)
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
- Currently supports ESP32

<a name="resources" />

Installation
-------------

- Download the repository from https://github.com/geekscape/aiko_engine and cd into it: `git clone https://github.com/geekscape/aiko_engine && cd aiko_engine`
- Ensure you have a [compatible board](https://micropython.org)
- Make sure you have a python [virtual environment set up](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) including [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper)
- Create (`mkvirtualenv upython`) and work on the new virtual environment `workon upython`
- Install AMPY from Adafruit `pip install -U adafruit-ampy`
- Plug in the ESP32 and make sure you can see it (eg `ls /dev/tty.*` provides eg `/dev/tty.wchserial1410`) 
- Export the port to a variable so AMPY can see it (`export AMPY_PORT=[port]` where `port` is the device address you had previously
- Run the aiko engine flash script `./scripts/flash_standard.sh`

Note for Lolin32lite boards - the serial port on this is notoriously problematic and requires a slight delay
in order for the connection to occur properly. If you're seeing errors that look like `ampy.pyboard.PyboardError: could not enter raw repl` then this is probably related.

In this case set a delay to sleep the board as it's uploading the files: `export AMPY_DELAY=4` will usually do the trick.

Resources
---------
Associated open-source ESP32 hardware ...

- [John Spencer's](https://twitter.com/mage0r)
  [LoliBot robot](https://github.com/mage0r/ESPkit-0://github.com/CCHS-Melbourne/LoliBot)
