#!/usr/bin/env python3
#
# Usage
# ~~~~~
# pip install pyserial transitions
#
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
#   Tester: (pass test.echo)
#
# To Do
# ~~~~~
# - Command line parameters for debug logging

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
        reset_test()
        write_all(COMMAND_IMPORT_TEST_MODULE.encode("utf-8"))

    def on_enter_ready(self, event_data):
        print("Tester and Testee are ready to begin testing")
        reset_test()

state_machine = None

PROMPT = ">>> "
TESTER = 0  # device id
TESTEE = 1  # device id
device_names = ["Tester", "Testee"]
serial_devices = [None, None]
serial_input = ["", ""]
serial_pathnames = [None, None]
repl_ready = [False, False]
test_passed = [False, False]

COMMAND_IMPORT_TEST_MODULE = "import aiko.test as test\r\n"
COMMAND_ECHO = "test.echo('(pass test.echo)')\r\n"
COMMAND_LOG = "test.log({})\r\n"
COMMAND_SET_GPIO_PIN_LIST = "test.set_gpio_pin_list({})\r\n"
COMMAND_GET_GPIO_PIN_LIST = "test.get_gpio_pin_list()\r\n"
COMMAND_SET_GPIO_PINS_MODE = "test.set_gpio_pins_mode({})\r\n"
COMMAND_GET_GPIO_PINS = "test.gpio_pins\r\n"
COMMAND_SET_GPIO_PINS_VALUE_LOW = "test.set_gpio_pins_value(0)\r\n"
COMMAND_SET_GPIO_PINS_VALUE_HIGH = "test.set_gpio_pins_value(1)\r\n"
COMMAND_SET_GPIO_PIN_VALUE_LOW = "test.set_gpio_pin_value({}, 0)\r\n"
COMMAND_SET_GPIO_PIN_VALUE_HIGH = "test.set_gpio_pin_value({}, 1)\r\n"
COMMAND_GET_GPIO_PINS_VALUE = "test.get_gpio_pins_value()\r\n"
COMMAND_SET_TOUCH_PIN_LIST = "test.set_touch_pin_list([12, 14])\r\n"
COMMAND_GET_TOUCH_PIN_LIST = "test.get_touch_pin_list() \r\n"
COMMAND_GET_TOUCH_PINS_VALUE = "test.get_touch_pins_value()\r\n"

last_pin_set = None

def check_all_pins_high(input):
    values_list = input[input.find("[") + 1:input.find("]")]
    gpio_values = [int(gpio_value) for gpio_value in values_list.split(",")]
    if not all(gpio_value == 1 for gpio_value in gpio_values):
        raise SystemExit("TEST FAILED: One or more pins are low")

def check_all_pins_low(input):
    values_list = input[input.find("[") + 1:input.find("]")]
    gpio_values = [int(gpio_value) for gpio_value in values_list.split(",")]
    if not all(gpio_value == 0 for gpio_value in gpio_values):
        raise SystemExit("TEST FAILED: One or more pins are high")

def check_pin_high(input):
    global last_pin_set
    values_list = input[input.find("[") + 1:input.find("]")]
    gpio_values = [int(gpio_value) for gpio_value in values_list.split(",")]
    if not gpio_values[last_pin_set]:
        raise SystemExit("TEST FAILED: GPIO pin is not high")
    gpio_values[last_pin_set] = 0
    if not all(gpio_value == 0 for gpio_value in gpio_values):
        raise SystemExit("TEST FAILED: Other pins are not low")

def check_pin_low(input):
    global last_pin_set
    values_list = input[input.find("[") + 1:input.find("]")]
    gpio_values = [int(gpio_value) for gpio_value in values_list.split(",")]
    if gpio_values[last_pin_set]:
        raise SystemExit("TEST FAILED: GPIO pin is not low")
    gpio_values[last_pin_set] = 1
    if not all(gpio_value == 1 for gpio_value in gpio_values):
        raise SystemExit("TEST FAILED: Other pins are not high")

def command_log(id, value):
    command = COMMAND_LOG.format(value)
    write_id(id, command.encode("utf-8"))

def command_set_gpio_pins_mode(id, value):
    command = COMMAND_SET_GPIO_PINS_MODE.format(value)
    write_id(id, command.encode("utf-8"))

def command_set_gpio_pin_list(id, value):
    command = COMMAND_SET_GPIO_PIN_LIST.format(value)
    write_id(id, command.encode("utf-8"))

def command_set_pin_low(id, value):
    global last_pin_set
    last_pin_set = value
    command = COMMAND_SET_GPIO_PIN_VALUE_LOW.format(value)
    write_id(id, command.encode("utf-8"))

def command_set_pin_high(id, value):
    global last_pin_set
    last_pin_set = value
    command = COMMAND_SET_GPIO_PIN_VALUE_HIGH.format(value)
    write_id(id, command.encode("utf-8"))

GPIO_PIN_LIST = "[19, 22, 33, 32, 23, 18, 25, 26, 2, 13]"
MODE_OUTPUT = 0
MODE_INPUT_PULL_DOWN = 1
MODE_INPUT_PULL_UP = 2

TEST_NAME = 0
DEVICE_ID = 1
COMMAND = 2
CHECK = 3
test_index = -1
tests = [
  ("test_00_0", TESTER, COMMAND_ECHO, None),
  ("test_00_1", TESTEE, COMMAND_ECHO, None),

  ("test_01_0", TESTER, command_log, "'TESTER BOARD'"),
  ("test_01_1", TESTEE, command_log, "'TESTEE BOARD'"),

  ("test_02_0", TESTER, command_set_gpio_pin_list, GPIO_PIN_LIST),
  ("test_02_1", TESTEE, command_set_gpio_pin_list, GPIO_PIN_LIST),

  ("test_03_0", TESTER, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_03_1", TESTER, COMMAND_SET_GPIO_PINS_VALUE_LOW, None),
  ("test_03_2", TESTEE, command_set_gpio_pins_mode, MODE_INPUT_PULL_UP),
  ("test_03_3", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_all_pins_low),

  ("test_04_0", TESTER, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_04_1", TESTER, COMMAND_SET_GPIO_PINS_VALUE_HIGH, None),
  ("test_04_2", TESTEE, command_set_gpio_pins_mode, MODE_INPUT_PULL_DOWN),
  ("test_04_3", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_all_pins_high),

  ("test_05_0", TESTEE, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_05_1", TESTEE, COMMAND_SET_GPIO_PINS_VALUE_LOW, None),
  ("test_05_2", TESTER, command_set_gpio_pins_mode, MODE_INPUT_PULL_UP),
  ("test_05_3", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_all_pins_low),

  ("test_06_0", TESTEE, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_06_1", TESTEE, COMMAND_SET_GPIO_PINS_VALUE_HIGH, None),
  ("test_06_2", TESTER, command_set_gpio_pins_mode, MODE_INPUT_PULL_DOWN),
  ("test_06_3", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_all_pins_high),

  ("test_07_00", TESTER, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_07_01", TESTER, COMMAND_SET_GPIO_PINS_VALUE_LOW, None),
  ("test_07_02", TESTEE, command_set_gpio_pins_mode, MODE_INPUT_PULL_DOWN),
  ("test_07_03", TESTER, command_set_pin_high, 0),
  ("test_07_04", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_05", TESTER, command_set_pin_low, 0),
  ("test_07_06", TESTER, command_set_pin_high, 1),
  ("test_07_07", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_08", TESTER, command_set_pin_low, 1),
  ("test_07_09", TESTER, command_set_pin_high, 2),
  ("test_07_10", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_11", TESTER, command_set_pin_low, 2),
  ("test_07_12", TESTER, command_set_pin_high, 3),
  ("test_07_13", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_14", TESTER, command_set_pin_low, 3),
  ("test_07_15", TESTER, command_set_pin_high, 4),
  ("test_07_16", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_17", TESTER, command_set_pin_low, 4),
  ("test_07_18", TESTER, command_set_pin_high, 5),
  ("test_07_19", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_20", TESTER, command_set_pin_low, 5),
  ("test_07_21", TESTER, command_set_pin_high, 6),
  ("test_07_22", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_23", TESTER, command_set_pin_low, 6),
  ("test_07_24", TESTER, command_set_pin_high, 7),
  ("test_07_25", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_26", TESTER, command_set_pin_low, 7),
  ("test_07_27", TESTER, command_set_pin_high, 8),
  ("test_07_28", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_29", TESTER, command_set_pin_low, 8),
  ("test_07_30", TESTER, command_set_pin_high, 9),
  ("test_07_31", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_07_32", TESTER, command_set_pin_low, 9),

  ("test_08_00", TESTER, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_08_01", TESTER, COMMAND_SET_GPIO_PINS_VALUE_HIGH, None),
  ("test_08_02", TESTEE, command_set_gpio_pins_mode, MODE_INPUT_PULL_UP),
  ("test_08_03", TESTER, command_set_pin_low, 0),
  ("test_08_04", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_05", TESTER, command_set_pin_high, 0),
  ("test_08_06", TESTER, command_set_pin_low, 1),
  ("test_08_07", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_08", TESTER, command_set_pin_high, 1),
  ("test_08_09", TESTER, command_set_pin_low, 2),
  ("test_08_10", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_11", TESTER, command_set_pin_high, 2),
  ("test_08_12", TESTER, command_set_pin_low, 3),
  ("test_08_13", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_14", TESTER, command_set_pin_high, 3),
  ("test_08_15", TESTER, command_set_pin_low, 4),
  ("test_08_16", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_17", TESTER, command_set_pin_high, 4),
  ("test_08_18", TESTER, command_set_pin_low, 5),
  ("test_08_19", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_20", TESTER, command_set_pin_high, 5),
  ("test_08_21", TESTER, command_set_pin_low, 6),
  ("test_08_22", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_23", TESTER, command_set_pin_high, 6),
  ("test_08_24", TESTER, command_set_pin_low, 7),
  ("test_08_25", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_26", TESTER, command_set_pin_high, 7),
  ("test_08_27", TESTER, command_set_pin_low, 8),
  ("test_08_28", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_29", TESTER, command_set_pin_high, 8),
  ("test_08_30", TESTER, command_set_pin_low, 9),
  ("test_08_31", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_08_32", TESTER, command_set_pin_high, 9),

  ("test_09_00", TESTEE, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_09_01", TESTEE, COMMAND_SET_GPIO_PINS_VALUE_LOW, None),
  ("test_09_02", TESTER, command_set_gpio_pins_mode, MODE_INPUT_PULL_DOWN),
  ("test_09_03", TESTEE, command_set_pin_high, 0),
  ("test_09_04", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_05", TESTEE, command_set_pin_low, 0),
  ("test_09_06", TESTEE, command_set_pin_high, 1),
  ("test_09_07", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_08", TESTEE, command_set_pin_low, 1),
  ("test_09_09", TESTEE, command_set_pin_high, 2),
  ("test_09_10", TESTEE, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_11", TESTEE, command_set_pin_low, 2),
  ("test_09_12", TESTEE, command_set_pin_high, 3),
  ("test_09_13", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_14", TESTEE, command_set_pin_low, 3),
  ("test_09_15", TESTEE, command_set_pin_high, 4),
  ("test_09_16", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_17", TESTEE, command_set_pin_low, 4),
  ("test_09_18", TESTEE, command_set_pin_high, 5),
  ("test_09_19", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_20", TESTEE, command_set_pin_low, 5),
  ("test_09_21", TESTEE, command_set_pin_high, 6),
  ("test_09_22", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_23", TESTEE, command_set_pin_low, 6),
  ("test_09_24", TESTEE, command_set_pin_high, 7),
  ("test_09_25", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_26", TESTEE, command_set_pin_low, 7),
  ("test_09_27", TESTEE, command_set_pin_high, 8),
  ("test_09_28", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_29", TESTEE, command_set_pin_low, 8),
  ("test_09_30", TESTEE, command_set_pin_high, 9),
  ("test_09_31", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_high),
  ("test_09_32", TESTEE, command_set_pin_low, 9),

  ("test_10_00", TESTEE, command_set_gpio_pins_mode, MODE_OUTPUT),
  ("test_10_01", TESTEE, COMMAND_SET_GPIO_PINS_VALUE_HIGH, None),
  ("test_10_02", TESTER, command_set_gpio_pins_mode, MODE_INPUT_PULL_UP),
  ("test_10_03", TESTEE, command_set_pin_low, 0),
  ("test_10_04", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_05", TESTEE, command_set_pin_high, 0),
  ("test_10_06", TESTEE, command_set_pin_low, 1),
  ("test_10_07", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_08", TESTEE, command_set_pin_high, 1),
  ("test_10_09", TESTEE, command_set_pin_low, 2),
  ("test_10_10", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_11", TESTEE, command_set_pin_high, 2),
  ("test_10_12", TESTEE, command_set_pin_low, 3),
  ("test_10_13", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_14", TESTEE, command_set_pin_high, 3),
  ("test_10_15", TESTEE, command_set_pin_low, 4),
  ("test_10_16", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_17", TESTEE, command_set_pin_high, 4),
  ("test_10_18", TESTEE, command_set_pin_low, 5),
  ("test_10_19", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_20", TESTEE, command_set_pin_high, 5),
  ("test_10_21", TESTEE, command_set_pin_low, 6),
  ("test_10_22", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_23", TESTEE, command_set_pin_high, 6),
  ("test_10_24", TESTEE, command_set_pin_low, 7),
  ("test_10_25", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_26", TESTEE, command_set_pin_high, 7),
  ("test_10_27", TESTEE, command_set_pin_low, 8),
  ("test_10_28", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_29", TESTEE, command_set_pin_high, 8),
  ("test_10_30", TESTEE, command_set_pin_low, 9),
  ("test_10_31", TESTER, COMMAND_GET_GPIO_PINS_VALUE, check_pin_low),
  ("test_10_32", TESTEE, command_set_pin_high, 9)
]

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
        raise SystemExit("All tests passed")

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
    global state_machine

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

    if state_machine.model.state == "ready" and input.startswith("(pass "):
        run_test(input)

    if input == "(pass aiko.test)":
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
