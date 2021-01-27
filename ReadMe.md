# Aiko Engine MP ([microPython](http://micropython.org))

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Resources](#resources)
## Pages
- [Contributors](Contributors.md)
- [Software license](License)

## Overview

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

## Installation

Installation is a three stage process:

1. Setup the correct tooling on your workstation
2. Download and install MicroPython onto your ESP32 development board
3. Install the Aiko software onto your ESP32 development board

### SETUP

- Make sure you have a current version of [Python3](https://www.python.org/) available on your workstation

- Download the Aiko software code from https://github.com/geekscape/aiko_engine_mp

```
    git clone https://github.com/geekscape/aiko_engine_mp
    cd aiko_engine_mp
```

  Note: If you don't have Git installed you download a zip file from https://github.com/geekscape/aiko_engine_mp

- Setup a [virtual Python environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) for your badge project

- Make sure your Python virtual environment is active

- Install Python packages [`esptool`](https://github.com/espressif/esptool/blob/master/README.md) and [`mpfshell`](https://github.com/wendlers/mpfshell/blob/master/README.md)
```
    pip install esptool
    pip install -U mpfshell
```

Note: For `mpfshell` (version v0.9.1 and earlier) on Mac OS X or Windows, this
problem may be fixed via this [patch](https://github.com/wendlers/mpfshell/commit/52b0636c82b06a07daa5731550f86b0d7ebc7608). You may find it easier to install `mpfshell`
manually from the [source](https://github.com/wendlers/mpfshell/blob/master/README.md#from-source)

### Download and install MicroPython

- Download the latest MicroPython binary for your ESP32 boardfrom https://micropython.org/download/

  Note that you must have a
    [compatible hardware board](https://github.com/micropython/micropython/wiki/Boards-Summary) or
    [compatible microPython port](https://github.com/micropython/micropython/tree/master/ports)


- Plug in your ESP32 device and make sure you can see it. For example on
  - macOS or Linux:
  `ls /dev/tty.*` provides something similar to `/dev/tty.wchserial1410`
  - On Windows, use the device manager to discover the COM port

![Example of using the Windows Device manager](/Windows-Device-Manager-Example.png)

- Export the serial port to an environment variable, so `mpfshell` can use it,
  e.g `export AMPY_PORT=<port>` or  `$env:AMPY_PORT = <port>` where `port` is the device address shown
  by the `ls` command above, or in the Windows device manager
- Flash microPython. Helper scripts are provided

```
    ./scripts/flash_micropython.sh
    .\scripts\windows\flash_micropython.ps1
```

### Install the Aiko software

- Run the Aiko Engine MP flash script

```
    ./scripts/mpf_script.sh ./scripts/aiko.mpf
    .\scripts\windows\mpf_script.ps1 scripts\aiko.mpf
```

Note: For Lolin32-Lite boards, the serial port can be notoriously problematic
and requires a slight delay in order for the connection to occur properly.
If you're seeing errors that look like `Could not enter raw repl` then this is probably related.

## Resources

Associated open-source ESP32 hardware projects ...

- [OHMC team's](https://twitter.com/swagbadge2021) -
  [LCA2021 SwagBadge](http://www.openhardwareconf.org/wiki/Swagbadge2021)
- [John Spencer's](https://twitter.com/mage0r) -
  [LCA2018 LoliBot robot](https://github.com/CCHS-Melbourne/LoliBot)
- [OHMC team's](http://www.openhardwareconf.org) -
  [LCA2017 IoTuz](http://www.openhardwareconf.org/wiki/OHC2017)