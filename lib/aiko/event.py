# lib/aiko/event.py: version: 2020-12-22 09:00 v05
#
# Usage
# ~~~~~
# import time
# import aiko.event as event
#
# def event_test():
#   print("event_test(): " + str(time.ticks_ms() / 1000))
#
# event.add_timer_handler(event_test, 1000)
# event.loop()
#
# To Do
# ~~~~~
# - Add flatout handler.
# - Add "handler_count" and "loop(loop_when_no_handlers=False)"
#
# - Provide helper function for running event.loop() in a background thread
#   - Consider implementing "lib/aiko/thread.py" manager
#
# - If "event_list.head.time_next" is above a given threshold, then deep sleep

from threading import Thread
import time                             # time.ticks_ms() takes 27 microseconds

class Event:
  def __init__(self, handler, time_period, immediate=False):
    self.handler = handler
    self.time_next = time.ticks_ms()
    if not immediate:
      self.time_next += time_period
    self.time_period = time_period
    self.next = None

  def __str__(self):
    output = "%s every %d next %d"
    return output % (self.handler, self.time_period, self.time_next)

class EventList:
  def __init__(self):
    self.head = None

  def add(self, event):
    if not self.head or event.time_next < self.head.time_next:
      event.next = self.head
      self.head = event
    else:
      current = self.head
      while current.next:
        if current.next.time_next > event.time_next: break
        current = current.next
      event.next = current.next
      current.next = event

  def print(self):
    current = self.head
    while current:
      print(current)
      current = current.next

  def remove(self, handler):
    previous = None
    current = self.head
    while current:
      if current.handler.__name__ == handler.__name__:
        if previous:
          previous.next = current.next
        else:
          self.head = current.next
        break
      previous = current
      current = current.next
    return current

  def reset(self):
    current = self.head
    current_time = time.ticks_ms()
    while current:
      current.time_next = current_time + current.time_period
      current = current.next

  def update(self):
    if self.head:
      event = self.head
      event.time_next += event.time_period
      if event.next:
        if event.time_next > event.next.time_next:
          self.head = event.next
          self.add(event)

event_enabled = False
event_list = EventList()

def add_timer_handler(handler, time_period, immediate=False):
  event = Event(handler, time_period, immediate)
  event_list.add(event)

def remove_timer_handler(handler):
  event_list.remove(handler)

def next_timer_event_gap():
  gap = 100  # default milliseconds, if no events
  event = event_list.head
  if event:
    gap = event.time_next - time.ticks_ms()
  return gap

def loop():
  global event_enabled
  event_list.reset()

  event_enabled = True
  while event_enabled:
    gap = next_timer_event_gap()
    while gap <= 0:
      event_list.head.handler()
      event_list.update()
      gap = next_timer_event_gap()
#   print("event:loop(): sleep " + str(gap))
    time.sleep_ms(gap)
    
def loop_thread():
  Thread(target=loop).start()

def terminate():
  global event_enabled
  event_enabled = False
