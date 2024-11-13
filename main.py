import json
import neopixel
from machine import Pin
from utils.connect_wifi import connect_to_wifi
from utils.websocket import Websocket
from utils.get_safest_path import get_safest_path
from utils.display_direction import display_direction
from utils.get_floor_plan import get_floor_plan

# Constants that can be changed from Serial monitor
# FLOOR_ID, NODE_ID, GAS_THRESHOLD, AIR_THRESHOLD

# Set up the NeoPixel on GPIO 18, with the number of LEDs in your strip
neo_pin = 18
num_leds = 24  # Replace with the number of LEDs in your NeoPixel strip

np = neopixel.NeoPixel(Pin(neo_pin), num_leds)

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

ws = Websocket(url, headers, subprotocols=subprotocols)
ws.initialize()

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

tasks.append(wrap_function(check_for_response))
tasks.append(wrap_function(on_message))

while tasks:
  for task in tasks:
    try:
      next(task)
    except StopIteration:
      tasks.remove(task)