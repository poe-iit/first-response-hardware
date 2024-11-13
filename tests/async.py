import machine
import time

led = machine.Pin(2, machine.Pin.OUT)
led.value(False)

def wrap_function(function, *args, **kwargs):
  while True:
    value = function(*args, **kwargs)
    yield value

def toggle_led():
  if led.value():
    led.value(False)
  else:
    led.value(True)
  time.sleep(5)

def print_time():
  print(time.time())
  time.sleep(3)

tasks = []
tasks.append(wrap_function(toggle_led))
tasks.append(wrap_function(print_time))

while tasks:
  for task in tasks:
    try:
      next(task)
    except StopIteration:
      tasks.remove(task)