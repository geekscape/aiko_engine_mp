# lib/aiko/queue.py: version: 2020-12-13 18:30 v04
#
# https://en.wikipedia.org/wiki/Stack-sortable_permutation
# https://en.wikipedia.org/wiki/Donald_Knuth

class Queue: 
  def __init__(self):
    self.stack_in = []
    self.stack_out = []

  def length(self):
    return len(self.stack_in) + len(self.stack_out)

  def push(self, item):
    self.stack_in.append(item)

  def pop(self):
    if self.length() == 0: return None
    if not self.stack_out:
      while self.stack_in:
        self.stack_out.append(self.stack_in.pop())
    return self.stack_out.pop()
