import json
import time
from utils.connect_wifi import connect_to_wifi
from utils.websocket import Websocket
from utils.get_safest_path import get_safest_path

connect_to_wifi("IIT-IoT", "IPRO-POE-ESP-32-1")

url = "wss://first-response-server-v2-0.onrender.com"
headers = {
  "Cookie": "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzBhMGI1MzNhOTkwN2U2Nzg5ZjJjYTMiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMTE4MTYzOSwiZXhwIjoxNzMxNDQwODM5fQ._shv-ROe6y0G4tJscW2R8Q7bevg0eWaAXgoMjwZlHGk; Path=/; Secure; HttpOnly; Expires=Sat, 16 Nov 2024 19:47:19 GMT;",
}
subprotocols = ["graphql-transport-ws"]

ws = Websocket(url, headers, subprotocols=subprotocols)

# Work on adding this as part of the init
message = {
  "type": "connection_init"
}
message = json.dumps(message).encode("utf-8")
ws.send_message(message)
response = ws.receive_message()
print("Message from server:", response)

try:
  # Set up

  # Subscribe to websocket events
  message = {
    "type": "subscribe",
    "payload": {
      "query": "subscription{sendHello{message}}"
    }
  }
  ws.subscribe(message)

  query = """
    subscription{
      floorUpdate(id: \"672fed9525894388bcf9dff1\"){
        name
        nodes {
          id
          state
          isExit
          connections{
            id
          }
          ui {
            x
            y
          }
        }
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
  while True:
    # Loop
    response = ws.receive_message()
    # ws.send_ping()
    # ws.send_pong()
    if response:
      print("Message from server:", response)
      response = json.loads(response)
      data = response.get("payload", {}).get("data", {})
      if data.get("floorUpdate"):
        print(get_safest_path(data.get("floorUpdate")))
      # Move this over to the websocket class and store the id for easier look
      # up on what data is being gotten


    # Pongs should be sent at least once every 10 seconds, but some operations
    # could take longer than that(so just incase I don't catch it)
    ws.send_pong()
    time.sleep(5)
except KeyboardInterrupt:
  print("Closing connection")
except OSError as err:
  print(err)
  print("Connection closed")
finally:
  # Cleanup
  ws.s.close()