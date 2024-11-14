import machine
import neopixel
from utils.load_env import load_env

env = load_env()

# Set up the NeoPixel, with the number of LEDs on strip
neo_dir_pin = int(env.get("NEO_PIXEL_DIR_PIN"))
neo_cross_pin = int(env.get("NEO_PIXEL_CROSS_PIN"))
num_leds = 24

np_dir = neopixel.NeoPixel(machine.Pin(neo_dir_pin), num_leds)
np_cross = neopixel.NeoPixel(machine.Pin(neo_cross_pin), num_leds)

def update_strip(np, strip, color):
  start = strip * (num_leds / 4)
  for i in range(0, int(num_leds / 4)):
    np[int(start + i)] = color
  np.write()

def reset_strip(np):
  for i in range(0, num_leds):
    np[i] = (0, 0, 0)
  np.write()

def display_direction(direction, color):
  print(direction, color)
  if direction == "left":
    reset_strip(np_dir)
    reset_strip(np_cross)
    update_strip(np_dir,0, color)
    update_strip(np_dir, 1, (0, 0, 0))
    update_strip(np_dir, 2, color)
    update_strip(np_dir, 3, (0, 0, 0))
  elif direction == "right":
    reset_strip(np_dir)
    reset_strip(np_cross)
    update_strip(np_dir, 0, (0, 0, 0))
    update_strip(np_dir, 1, color)
    update_strip(np_dir, 2, (0, 0, 0))
    update_strip(np_dir, 3, color)
  elif direction == "up":
    reset_strip(np_dir)
    reset_strip(np_cross)
    update_strip(np_dir, 0, (0, 0, 0))
    update_strip(np_dir, 1, color)
    update_strip(np_dir, 2, color)
    update_strip(np_dir, 3, (0, 0, 0))
  elif direction == "down":
    reset_strip(np_dir)
    reset_strip(np_cross)
    update_strip(np_dir, 0, color)
    update_strip(np_dir, 1, (0, 0, 0))
    update_strip(np_dir, 2, (0, 0, 0))
    update_strip(np_dir, 3, color)
  elif direction == "cross":
    reset_strip(np_dir)
    reset_strip(np_cross)
    update_strip(np_cross, 0, color)
    update_strip(np_cross, 1, color)
    update_strip(np_cross, 2, color)
    update_strip(np_cross, 3, color)
  else:
    reset_strip(np_dir)
    reset_strip(np_cross)
    update_strip(np_dir, 0, color)
    update_strip(np_dir, 1, color)
    update_strip(np_dir, 2, color)
    update_strip(np_dir, 3, color)
