import asyncio
import websockets
import json

# Handler function that will be called whenever a new message is received
async def on_message(message):
  print(f"Received message: {message}")
  # Process the message here as needed

# Message listener coroutine that will run in the background
async def message_listener(websocket):
  while True:
    message = await websocket.recv()
    await on_message(message)

# Main function to connect and initialize the WebSocket connection
async def receive_messages():
  async with websockets.connect(
    "wss://first-response-server-v2-0.onrender.com",
    subprotocols=["graphql-transport-ws"],
    extra_headers=[("Cookie", "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzBhMGI1MzNhOTkwN2U2Nzg5ZjJjYTMiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMDk1NzE0MSwiZXhwIjoxNzMxMjE2MzQxfQ.t4gIWDM_dxy1XJenMO6nMPgsLaR-3CBGNt8CE88rYrY; Path=/; Secure; HttpOnly; Expires=Thu, 14 Nov 2024 05:25:41 GMT;")]
  ) as websocket:
    # Send connection initialization
    await websocket.send('{"type": "connection_init"}')
    
    # Wait for connection acknowledgment
    while True:
      message = await websocket.recv()
      message = json.loads(message)
      if message["type"] == "connection_ack":
        print("Connection acknowledged.")
        break

    # Send subscription request
    request = json.dumps({
      "id": "ad",
      "type": "subscribe",
      "payload": {
        "query": "subscription{sendHello{message}}"
      }
    })
    await websocket.send(request)
    
    # Start the message listener and other tasks concurrently
    await asyncio.gather(
      message_listener(websocket),  # Runs the message listener in the background
      main()                 # Placeholder for other tasks you want to run concurrently
    )

# Example of other tasks to run concurrently with the WebSocket listener
async def main():
  while True:
    await asyncio.sleep(5)
    print("Performing main tasks...")

# Run the main function
asyncio.run(receive_messages())
