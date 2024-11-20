class EventLoop:
  def __init__(self):
    self.queue = []
  
  def wrap_task(self, function, *args, **kwargs):
    while True:
      value = function(*args, **kwargs)
      yield value
  
  def run_until_complete(self):
    while self.queue:
      for task in self.queue:
        try:
          next(task)
        except StopIteration:
          print("Task complete", task)
          self.queue.remove(task)

  def create_task(self, coro):
    self.queue.append(
      self.wrap_task(coro)
    )
  
  def add_task(self, task, *args, **kwargs):
    self.queue.append(task(*args, **kwargs))