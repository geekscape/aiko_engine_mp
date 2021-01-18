#!/usr/bin/env python3
#
# Usage
# ~~~~~
# pip install pyserial transitions
#
# ./scripts/device_info.py dev/tty.wchusbserial1450
#
# To Do
# ~~~~~
# - Provide more details, e.g Aiko version number
# - Validate all file versions

import select
import serial
import sys
import time
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
        print("Importing test module")
        reset_test()
        write_all(COMMAND_IMPORT_TEST_MODULE.encode("utf-8"))

    def on_enter_ready(self, event_data):
        print("Ready to begin testing")
        reset_test()

state_machine = None
serial_ids = ["unknown"]

PROMPT = ">>> "
device_names = ["device"]
serial_devices = [None]
serial_input = [""]
serial_pathnames = [None]
repl_ready = [False]
test_passed = [False]

COMMAND_IMPORT_TEST_MODULE = "import aiko.test as test\r\n"
COMMAND_ECHO = "test.echo('(pass test.echo)')\r\n"
COMMAND_LOG = "test.log({})\r\n"

last_pin_set = None

def command_log(id, value):
    command = COMMAND_LOG.format(value)
    write_id(id, command.encode("utf-8"))

TEST_NAME = 0
DEVICE_ID = 1
COMMAND = 2
CHECK = 3
test_index = -1
tests = []

def reset_test():
    test_passed = [False, False]

def run_test(input):
    global test_index

    if test_index >= 0:
        test = tests[test_index]
        if callable(test[CHECK]):
            test[CHECK](input)

    test_index += 1
    if test_index < len(tests):
        test = tests[test_index]
        print(f"Run test: {test[TEST_NAME]}")
        if type(test[COMMAND]) == str:
            write_id(test[DEVICE_ID], test[COMMAND].encode("utf-8"))
        if callable(test[COMMAND]):
            test[COMMAND](test[DEVICE_ID], test[CHECK])
    else:
        raise SystemExit("All tests passed: " + str(serial_ids))

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

    serial_device.setDTR(False)
    time.sleep(0.25)
    serial_device.setDTR(True)
    return serial_device

def process_input(id):
    input_count = serial_devices[id].in_waiting
    try:
        input = serial_devices[id].read(input_count).decode("utf-8")
    except UnicodeDecodeError:
#       print(f"{Unicode Decode Error")
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
    global state_machine

#   if True:
#   if id == TESTER:
#   if id == TESTEE:
    if input.startswith("("):
        print(f"{input}")

    if input.startswith("rst"):
        print(f"ESP32 booting")

    if "Pro cpu up." in input:
        print(f"microPython booting")

#   if input.startswith(PROMPT) and not repl_ready[id]:
    if input.startswith("MicroPython") and not repl_ready[id]:
        repl_ready[id] = True
        print(f"microPython REPL ready")
        if all(repl_ready):
            state_machine.dispatch("import")

    if state_machine.model.state == "ready" and input.startswith("(pass "):
        run_test(input)

    if input.startswith("(pass aiko.test"):
        tokens = input[1:-1].split()
        if len(tokens) > 2:
            serial_ids[id] = tokens[2]

        test_passed[id] = True
        if all(test_passed):
            state_machine.dispatch("ready")
            run_test(None)

def write_all(output):
    for id in range(len(device_names)):
        write_id(id, output)

def write_id(id, output):
    serial_devices[id].write(output)

def main():
    global state_machine
    model = StateMachineModel()
    state_machine = Machine(
        model=model,
        states=model.states,
        transitions=model.transitions,
        initial="start",
        send_event=True
    )

    device_fileno_id = {}
    poller = select.poll()
    for id in range(len(device_names)):
        serial_devices[id] = open_serial_device(serial_pathnames[id])
        print(f"{serial_pathnames[id]}")
        poller.register(serial_devices[id], select.POLLIN)
        device_fileno_id[serial_devices[id].fileno()] = id

    while True:
        fileno_events = poller.poll(5000)
        if len(fileno_events):
            for fileno_event in fileno_events:
                device_id = device_fileno_id[fileno_event[0]]
                process_input(device_id)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: device_info.py DEVICE_PATHNAME")
    serial_pathnames[0] = sys.argv[1]
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("KeyboardInterrupt: abort !")
