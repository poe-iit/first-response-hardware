import json
import _thread
import time
from machine import Pin
from utils.load_env import load_env
from utils.connect_wifi import connect_to_wifi
from utils.websocket import Websocket
from utils.get_safest_path import get_safest_path
from utils.display_direction import display_direction
from utils.get_floor_plan import get_floor_plan
from utils.event_loop import EventLoop
from utils.audio import Alarm

env = load_env()
help(_thread)

# Get environment variables
ssid = env.get("WIFI_SSID")
password = env.get("WIFI_PASSWORD")
floor_id = env.get("FLOOR_ID")
node_id = env.get("NODE_ID")
server_url = env.get("SERVER_URL")

event_loop = EventLoop()

# Constants that can be changed from Serial monitor
# FLOOR_ID, NODE_ID, GAS_THRESHOLD, AIR_THRESHOLD


state_colors = {
  "safe": (2, 119, 189),
  "compromised": (230, 57, 70),
  "stuck": (255, 136, 0),
  "exit": (76, 175, 80)
}

websocket_message = None
state = "safe"
# Work on updating logic to use name instead of id

# Setup
connect_to_wifi(ssid, password)

url = f"wss://{server_url}"
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
    state, direction = get_safest_path(node_id, data.get("getFloorPlan"))
    display_direction(direction, state_colors.get(state))

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
  global websocket_message, state
  if websocket_message:
    data = websocket_message.get("payload", {}).get("data", {})
    # Maybe a switch statement would be more intuitive
    if data.get("floorUpdate"):
      state, direction = get_safest_path(node_id, data.get("floorUpdate"))
      display_direction(direction, state_colors.get(state))
  websocket_message = None

def alarm_task(*args, **kwargs):
  alarm = Alarm(*args, **kwargs)
  while True:
    # if state == "compromised":
    alarm.play_alarm(4)
    time.sleep(0.8)  # Interval between alarms

_thread.start_new_thread(alarm_task, (2200, 0.12, 0.65))

event_loop.create_task(check_for_response)
event_loop.create_task(on_message)

event_loop.run_until_complete()