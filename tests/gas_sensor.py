import time
from machine import Pin
from utils.load_env import load_env

env = load_env()

gas_sensor_pin = Pin(21)
while True:
  print(gas_sensor_pin.value())
  time.sleep(1)