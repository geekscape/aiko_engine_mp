#!/usr/bin/env python3
#
# Usage
# ~~~~~
# TESTER_PATHNAME = /dev/tty.wchusbserial1440
# TESTEE_PATHNAME = /dev/tty.wchusbserial1450
# ./scripts/tester.py $TESTER_PATHNAME $TESTEE_PATHNAME
#   Tester: /dev/tty.wchusbserial1440
#   Testee: /dev/tty.wchusbserial1450
#   Tester: microPython booting
#   Tester: microPython REPL ready
#   Tester and Testee importing test module
#   Tester: (pass aiko.test)
#   Tester and Testee are ready to begin testing
#
# To Do
# ~~~~~
# - None, yet !
#
# test.set_gpio_pin_list([19, 22])   # Set list of GPIO pin numbers
# test.get_gpio_pin_list()           # Get list of GPIO pin numbers
# test.set_gpio_pins_mode(0)         # GPIO mode: Output
# test.set_gpio_pins_mode(1)         # GPIO mode: Input pull-down
# test.set_gpio_pins_mode(2)         # GPIO mode: Input pull-up
# test.gpio_pins                     # Check GPIO pins have been initialised
# test.set_gpio_pins_value(0)        # Set all GPIO pins low
# test.set_gpio_pins_value(1)        # Set all GPIO pins high
# test.set_gpio_pin_value(index, 0)  # Set single GPIO pin[index] low
# test.set_gpio_pin_value(index, 1)  # Set single GPIO pin[index] high
# test.get_gpio_pins_value()         # Check all GPIO pin input values
#
# test.set_touch_pin_list([12, 14])  # Set list of touch pin numbers
# test.get_touch_pin_list()          # Get list of touch pin numbers
# test.get_touch_pins_value()        # Check all touch pin input values

import select
import serial
import sys
from transitions import Machine
from transitions.core import MachineError

class StateMachineModel(object):
    states = [
        "start",
        "import",
        "ready"
    ]

    transitions = [
        {"source": "start",  "trigger": "import", "dest": "import"},
        {"source": "import", "trigger": "ready",  "dest": "ready"}
    ]

    def on_enter_import(self, event_data):
        print("Tester and Testee importing test module")
        test_reset()
        write_all(COMMAND_IMPORT_TEST_MODULE)

    def on_enter_ready(self, event_data):
        print("Tester and Testee are ready to begin testing")
        test_reset()
        write_all(COMMAND_TEST_ECHO)

model = StateMachineModel()

state_machine = Machine(
    model=model,
    states=model.states,
    transitions=model.transitions,
    initial="start",
    send_event=True
)

COMMAND_IMPORT_TEST_MODULE = """
import aiko.test as test\r\n
""".encode("utf-8")

COMMAND_TEST_ECHO = """
test.echo("(Go away, I'm busy !)")\r\n
""".encode("utf-8")

PROMPT = ">>> "
TESTER = 0  # device id
TESTEE = 1  # device id
device_names = ["Tester", "Testee"]
serial_devices = [None, None]
serial_input = ["", ""]
serial_pathnames = [None, None]
repl_ready = [False, False]
test_passed = [False, False]

def test_reset():
    test_passed = [False, False]

def open_serial_device(serial_pathname):
    try:
        serial_device = serial.Serial(
            port=serial_pathname,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            timeout=None,
            writeTimeout=0
        )
    except serial.serialutil.SerialException:
        raise SystemExit("Couldn't open serial device: " + serial_pathname)

    if not serial_device.isOpen():
        raise SystemExit("Serial device isn't open: " + serial_pathname)
    return serial_device

def process_input(id):
    input_count = serial_devices[id].in_waiting
    try:
        input = serial_devices[id].read(input_count).decode("utf-8")
    except UnicodeDecodeError:
#       print(f"{device_names[id]}: Unicode Decode Error")
        return

    serial_input[id] += input
    if not "\r\n" in serial_input[id]:
        return

    records = serial_input[id].split("\r\n")
    if not records[-1]:          # input ended with CR-LF
        serial_input[id] = ""
    elif records[-1] == PROMPT:  # Python prompt without CR-LF
        serial_input[id] = ""
        records.append("")
    else:                        # incomplete input, no CR-LF
        serial_input[id] = records[-1]
    records = records[:-1]

    for record in records:
        if record.startswith(PROMPT):
            parse_input(id, PROMPT)
            record = record[4:]
        if not record:
            continue
        parse_input(id, record)

def parse_input(id, input):
#   if True:
#   if id == TESTER:
#   if id == TESTEE:
    if input.startswith("("):
        print(f"{device_names[id]}: {input}")

    if input.startswith("rst"):
        print(f"{device_names[id]}: ESP32 booting")

    if "Pro cpu up." in input:
        print(f"{device_names[id]}: microPython booting")

#   if input.startswith(PROMPT) and not repl_ready[id]:
    if input.startswith("MicroPython") and not repl_ready[id]:
        repl_ready[id] = True
        print(f"{device_names[id]}: microPython REPL ready")
        if all(repl_ready):
            state_machine.dispatch("import")

    if input == "(pass aiko.test)":
        test_passed[id] = True
        if all(test_passed):
            state_machine.dispatch("ready")

def write_all(output):
    for id in range(len(device_names)):
        write_id(id, output)

def write_id(id, output):
    serial_devices[id].write(output)

def main():
    device_fileno_id = {}
    poller = select.poll()
    for id in range(len(device_names)):
        serial_devices[id] = open_serial_device(serial_pathnames[id])
        print(f"{device_names[id]}: {serial_pathnames[id]}")
        poller.register(serial_devices[id], select.POLLIN)
        device_fileno_id[serial_devices[id].fileno()] = id

    while True:
        fileno_events = poller.poll(5000)
        if len(fileno_events):
            for fileno_event in fileno_events:
                device_id = device_fileno_id[fileno_event[0]]
                process_input(device_id)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: tester.py TESTER_PATHNAME  TESTEE_PATHNAME")
    serial_pathnames[TESTER] = sys.argv[1]
    serial_pathnames[TESTEE] = sys.argv[2]
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("KeyboardInterrupt: abort !")
