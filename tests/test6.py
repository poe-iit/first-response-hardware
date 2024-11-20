import json
import time
import neopixel
import random
import math
from machine import Pin
# from machine import UART
from utils.connect_wifi import connect_to_wifi
from utils.websocket import Websocket
from utils.get_safest_path import get_safest_path
from utils.display_direction import display_direction
from utils.floor_plan import get_floor_plan

# Constants that can be changed from Serial monitor
# FLOOR_ID, NODE_ID, GAS_THRESHOLD, AIR_THRESHOLD

# Set up the NeoPixel on GPIO 18, with the number of LEDs in your strip
neo_pin = 18
num_leds = 24  # Replace with the number of LEDs in your NeoPixel strip

np = neopixel.NeoPixel(Pin(neo_pin), num_leds)

# serial_port = "COM6"

# Example to turn on the first LED with red color
np[0] = (255, 0, 0)  # RGB format
np[1] = (0, 255, 0)
np[2] = (0, 0, 255)
np[3] = (255, 0, 0)  # RGB format
np[4] = (0, 255, 0)
np[5] = (0, 0, 255)
np[6] = (255, 0, 0)  # RGB format
np[7] = (0, 255, 0)
np[8] = (0, 0, 255)
np[9] = (255, 0, 0)  # RGB format
np[10] = (0, 255, 0)
np[11] = (0, 0, 255)
np[12] = (255, 0, 0)  # RGB format
np[13] = (0, 255, 0)
np[14] = (0, 0, 255)
np[15] = (255, 0, 0)  # RGB format
np[16] = (0, 255, 0)
np[17] = (0, 0, 255)
np[1] = (255, 0, 0)  # RGB format
np[19] = (0, 255, 0)
np[20] = (0, 0, 255)
np[21] = (255, 0, 0)  # RGB format
np[22] = (0, 255, 0)
np[23] = (0, 0, 255)

np.write()

def wrap_function(function, *args, **kwargs):
  while True:
    value = function(*args, **kwargs)
    yield value

tasks = []
websocket_message = None
# Work on updating logic to use name instead of id
node_id = "673257c76f536ffcdeb7c4df"
floor_id = "673257c76f536ffcdeb7c4da"
directions = ["up", "down", "left", "right"]
direction = 0
# uart = UART(1, baudrate=9600, parity=None, stop=1, tx=17, rx=16)
# help(uart)
# uart.init(115200, bits=8, parity=None, stop=1)
# help("modules")
# ser = serial.Serial(serial_port, 9600, timeout=1)
# Setup
connect_to_wifi("IIT-IoT", "IPRO-POE-ESP-32-1")

url = "wss://first-response-server-v2-0.onrender.com"
headers = {
  "Cookie": "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzBhMGI1MzNhOTkwN2U2Nzg5ZjJjYTMiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMTQwNDkyMCwiZXhwIjoxNzMxNjY0MTIwfQ.-nHidtNAT_z_kvvv5wCZI8nbpZacL_cjVTr5PEwtYB8; Path=/; Secure; HttpOnly; Expires=Tue, 19 Nov 2024 09:48:40 GMT;",
}
subprotocols = ["graphql-transport-ws"]

response = get_floor_plan(floor_id, headers)
if response:
  response = json.loads(response)
  data = response.get("data", {})
  # Maybe a switch statement would be more intuitive
  if data.get("getFloorPlan"):
    color, direction = get_safest_path(node_id, data.get("getFloorPlan"))
    display_direction(direction, color)

help("modules")

ws = Websocket(url, headers, subprotocols=subprotocols)
ws.initialize()
query = """
  subscription{
    sendHello{
      message
    }
  }
"""

message = {
  "type": "subscribe",
  "payload": {
    "query": query
  }
}
ws.subscribe(message)

query = f"""
  subscription{{
    floorUpdate(id: \"{floor_id}\"){{
      name
      nodes {{
        id
        state
        isExit
        connections{{
          id
          name
          direction
        }}
        ui {{
          x
          y
        }}
      }}
    }}
  }}
"""
message = {
  "type": "subscribe",
  "payload": {
    "query": query
  }
}
ws.subscribe(message)


def check_for_response():
  global websocket_message
  response = ws.receive_message()
  # ws.send_ping()
  # ws.send_pong()
  if response:
    print("Message recieved from socket")
    response = json.loads(response)
    websocket_message = response

def on_message():
  global websocket_message
  if websocket_message:
    data = websocket_message.get("payload", {}).get("data", {})
    # Maybe a switch statement would be more intuitive
    if data.get("floorUpdate"):
      color, direction = get_safest_path(node_id, data.get("floorUpdate"))
      display_direction(direction, color)
  websocket_message = None

# def toggle_led():
#   global direction
#   red = math.ceil(random.random() * 255)
#   green = math.ceil(random.random() * 255)
#   blue = math.ceil(random.random() * 255)
#   print(directions[direction], (red, green, blue))
#   display_direction(directions[direction], (red, green, blue))
#   if direction == 3:
#     direction = 0
#   else:
#     direction += 1

# Message should be in this format: ARG:VALUE
# Read message from serial monitor
# def read_serial():
#   global uart
#   uart.write(b"Hello from ESP32!\n")
#   message = uart.readline()
#   print("Getting message")
#   if message:
#     print(message.decode("utf-8"))


tasks.append(wrap_function(check_for_response))
tasks.append(wrap_function(on_message))
# tasks.append(wrap_function(toggle_led))
# tasks.append(wrap_function(read_serial))

while tasks:
  for task in tasks:
    try:
      next(task)
    except StopIteration:
      tasks.remove(task)
