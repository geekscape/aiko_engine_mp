# lib/aiko/event.py: version: 2018-02-11 00:00
#
# Usage
# ~~~~~
# import time
# import aiko.event as event
#
# def event_test(): 
#   print("event_test(): " + str(time.ticks_ms() / 1000))
#
# event.add_event_handler(event_test, 1000)
# event.loop() 
#
# To Do
# ~~~~~
# - Provide helper function for running event.loop() in a background thread
#   - Consider implementing "lib/aiko/thread.py" manager
#
# - If "event_list.head.time_next" is above a given threshold, then deep sleep

import machine

from time import ticks_ms  # 27 microseconds

timer = None
timer_id = -1   # Hardware timers: 0 to 3, Virtual timers: -1 ...
timer_counter = 0

def irq_handler(timer):
  global timer_counter
  timer_counter -= 1

def update_timer_counter():
  global timer_counter
  if event_list.head:
    timer_counter_new = event_list.head.time_next - ticks_ms()
    irq_state = machine.disable_irq()
    timer_counter = timer_counter_new
    machine.enable_irq(irq_state)

class Event:
  def __init__(self, handler, time_period):
    self.handler = handler
    self.time_next = ticks_ms() + time_period
    self.time_period = time_period
    self.next = None

class EventList:
  def __init__(self):
    self.head = None

  def add(self, event):
    if not self.head or event.time_next < self.head.time_next:
      event.next = self.head
      self.head = event
      update_timer_counter()
    else:
      current = self.head
      while current.next:
        if current.next.time_next > event.time_next: break
        current = current.next
      event.next = current.next
      current.next = event

  def remove(self, handler):
    previous = None
    current = self.head
    while current:
      if current.handler == handler:
        if previous:
          previous.next = current.next
        else:
          self.head = current.next
          update_timer_counter()
        break
      previous = current
      current = current.next
    return current

  def update(self):
    if self.head:
      event = self.head
      event.time_next += event.time_period
      if event.next:
        if event.time_next > event.next.time_next:
          self.head = event.next
          self.add(event)
      update_timer_counter()

event_enabled = False
event_list = EventList()

def add_event_handler(handler, time_period):
  event = Event(handler, time_period)
  event_list.add(event)

def remove_event_handler(handler):
  event_list.remove(handler)

def loop():
  global event_enabled, timer

  if not timer:
    timer = machine.Timer(timer_id)
    timer.init(mode=machine.Timer.PERIODIC, period=1, callback=irq_handler)
  update_timer_counter()

  event_enabled = True
  while event_enabled:
    event = event_list.head
    if event and timer_counter <= 0:
      if ticks_ms() >= event.time_next:
        event.handler()
        event_list.update()

def terminate():
  global event_enabled, timer
  event_enabled = False

  if timer:
    timer.deinit()
    timer = None
