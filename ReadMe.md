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
3. Install the Aiko software onto your ESP32 development board.

**Notes**:

* If you are using Linux or macOS then you will be using a Posix shell (e.g. [Bash](https://www.gnu.org/software/bash/) or [zsh](http://zsh.sourceforge.net/))
* If you are on Windows then we assume you are using [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview) on Windows 10.

### 1. Setup

- Make sure you have a current version of [Python3](https://www.python.org/) available on your workstation

- Download the Aiko software code from https://github.com/geekscape/aiko_engine_mp

```
    git clone https://github.com/geekscape/aiko_engine_mp
```
**Note**: If you don't have Git installed you can download a zip file from https://github.com/geekscape/aiko_engine_mp and unpack it


```
    cd aiko_engine_mp
```

**Note**: All commands below assume that `.../aiko_engine_mp` is your current directory.


- Setup a [virtual Python environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) for your badge project. e.g.

```
python3 -m venv .venv
```

- Make sure your Python virtual environment is active. **Note**: Do this every time a new terminal session is started

```
. .venv/bin/activate # Linux and macOS
. .venv\Scripts\activate.ps1 # Windows
```

- Install Python packages [`esptool`](https://github.com/espressif/esptool/blob/master/README.md) and [`mpfshell`](https://github.com/wendlers/mpfshell/blob/master/README.md)

```
pip install -r requirements.txt
```

**Notes**:

1. Some environments may need to install additional tools and libraries. e.g. on Debian or Ubuntu

```
sudo apt-get install -y libpython3-dev libffi-dev libssl-dev
```

2. You might find it useful to install an MQTT client for later use. There are packages [here](https://hivemq.github.io/mqtt-cli/docs/installation/packages.html).

### 2. Download and install MicroPython

- Download the latest MicroPython binary for your ESP32 board from https://micropython.org/download/

  Note that you must have a
    [compatible hardware board](https://github.com/micropython/micropython/wiki/Boards-Summary) or
    [compatible microPython port](https://github.com/micropython/micropython/tree/master/ports)

- Plug in your ESP32 device and make sure you can see it. For example on
  - macOS or Linux:
  `ls /dev/tty.*` provides something similar to `/dev/tty.wchserial1410`
  - On Windows, use the command `change port /query` to discover the COM port.

- Export the serial port to an environment variable, so helpder sripts can use it,
  e.g `export AMPY_PORT=<port>` or  `$env:AMPY_PORT = COM<n>` where `port` is the device address shown
  by the `ls` command above, or `COM<n>` is the serial port show by the command `change port` above.  **Note**: Do this every time a new terminal session is started

- Flash microPython. Helper scripts are provided

```
    ./scripts/flash_micropython.sh
    .\scripts\windows\flash_micropython.ps1
```

### 3. Install the Aiko software

- Run the Aiko Engine MP flash script

```
    ./scripts/mpf_script.sh ./scripts/aiko.mpf # Linux or macOS
    .\scripts\windows\mpf_script.ps1 .\scripts\aiko.mpf # Windows
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