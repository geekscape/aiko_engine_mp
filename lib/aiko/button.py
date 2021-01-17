# lib/aiko/button.py: version: 2020-01-17 17:00 v05
#
# Usage
# ~~~~~
# import aiko.button
# aiko.button.initialise()
# def handler(number, state):
#   print("Button {}: {}".format(number, "press" if state else "release"))
# aiko.button.add_button_handler(handler, [16, 17])
# aiko.button.add_touch_handler(handler, [12, 14, 15, 27])
# aiko.button.remove_handler(handler)
#
# To Do
# ~~~~~
# - After remove_handler(), can't re-use existing Button ?!?
# - Add short versus long button press
# - Add holding down multiple buttons simultaneously
# - Add touch slider support
# - Fix remove_handler(): Clean-up Button, when no handlers left

from machine import disable_irq, enable_irq, Pin, TouchPad

import aiko.event as event

buttons = []
pin_numbers = []
pins = []
pins_active = []  ### globally shared and writable by interrupt handler ###
touch_buttons = []

class Button:
  def __init__(self, driver, pin_number):
    self.driver = driver  # Pin or TouchPad
    self.pin_number = pin_number
    self.handlers = []
    self.state = False

  def call_handlers(self):
    for handler in self.handlers:
      handler(self.pin_number, self.state)

  def get_state(self):
    return self.state

  def set_state(self, state):
    self.state = state

  def value(self):
    result = None
    if isinstance(self.driver, Pin):
      result = self.driver.value()
    if isinstance(self.driver, TouchPad):
      result = self.driver.read() >= 200
    return result

def add_button_handler(handler, gpio_pin_numbers):
  for pin_number in gpio_pin_numbers:
    if pin_number in pin_numbers:
      button = buttons[pin_numbers.index(pin_number)]
      if not isinstance(button, Pin):
        raise Exception("Existing button {} isn't GPIO".format(pin_number))
    else:
      pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
      pin.irq(lambda p:pin_change_handler(p),
                trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
      button = create_button(pin, pin_number)

    button.handlers.append(handler)

def add_touch_handler(handler, touch_pin_numbers):
  for pin_number in touch_pin_numbers:
    if pin_number in pin_numbers:
      button = buttons[pin_numbers.index(pin_number)]
      if not isinstance(button, TouchPad):
        raise Exception("Existing button {} isn't TouchPad".format(pin_number))
    else:
      touch_pad = TouchPad(Pin(pin_number))
      button = create_button(touch_pad, pin_number)
      touch_buttons.append(button)

    button.handlers.append(handler)

def create_button(pin, pin_number):
  pin_numbers.append(pin_number)
  pins.append(pin)
  button = Button(pin, pin_number)
  buttons.append(button)
  return button

def remove_handler(handler):
  for button in buttons:
    if handler in button.handlers:
      button.handlers.remove(handler)

def button_handler():  # software timer event handler
# microPython doesn't support TouchPad interrupts :(
  for touch_button in touch_buttons:
    if not touch_button.value():
      if not touch_button.get_state():
        irq_state = disable_irq()
        pins_active.append(touch_button.driver)
        enable_irq(irq_state)

  irq_state = disable_irq()
  local_pins_active = [pin for pin in pins_active]
  enable_irq(irq_state)

  for pin in local_pins_active:
    button = buttons[pins.index(pin)]
    if button.value():  # Button no longer active
      irq_state = disable_irq()
      pins_active.remove(pin)
      enable_irq(irq_state)
      button.set_state(False)
      button.call_handlers()
    elif not button.get_state():
      button.set_state(True)
      button.call_handlers()

def pin_change_handler(pin):  # hardware pin interrupt handler
  if not pin.value():
    if not pin in pins_active:
      pins_active.append(pin)

def initialise():  # settings=configuration.button.settings
  event.add_timer_handler(button_handler, 200)  # 5 Hz
