import machine
import neopixel

# Set up the NeoPixel on GPIO 18, with the number of LEDs in your strip
neo_pin = 18
num_leds = 24  # Replace with the number of LEDs in your NeoPixel strip

np = neopixel.NeoPixel(machine.Pin(neo_pin), num_leds)

def update_strip(strip, color):
  start = strip * (num_leds / 4)
  for i in range(0, int(num_leds / 4)):
    np[int(start + i)] = color
  np.write()


def display_direction(direction, color):
  print(direction, color)
  if direction == "left":
    update_strip(0, color)
    update_strip(1, (0, 0, 0))
    update_strip(2, color)
    update_strip(3, (0, 0, 0))
  elif direction == "right":
    update_strip(0, (0, 0, 0))
    update_strip(1, color)
    update_strip(2, (0, 0, 0))
    update_strip(3, color)
  elif direction == "up":
    update_strip(0, (0, 0, 0))
    update_strip(1, color)
    update_strip(2, color)
    update_strip(3, (0, 0, 0))
  elif direction == "down":
    update_strip(0, color)
    update_strip(1, (0, 0, 0))
    update_strip(2, (0, 0, 0))
    update_strip(3, color)
  else:
    update_strip(0, color)
    update_strip(1, color)
    update_strip(2, color)
    update_strip(3, color)
