import os

# Change to the root directory
os.chdir('/')

# List and print contents of the root directory
root_contents = os.listdir('/')
print("Root directory contents:", root_contents)

# List files and folders in the root directory
for item in os.ilistdir('/'):
  print(item)  # Each 'item' is a tuple with details about the file/folder

# import time
# import websockets
# import json

# # A simple coroutine wrapper for sleep, to yield back to the event loop
# async def sleep(duration):
#   start = time.ticks_ms()
#   while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
#     yield  # Yield control back to the event loop

# # A custom event loop
# class EventLoop:
#   def __init__(self):
#     self.tasks = []

#   # Add a coroutine to the task list
#   def create_task(self, coroutine):
#     self.tasks.append(coroutine)

#   # Run the event loop until all tasks are done
#   def run_forever(self):
#     while self.tasks:
#       for task in list(self.tasks):  # Copy to avoid modification during iteration
#         try:
#           next(task)  # Run until the next yield
#         except StopIteration:
#           self.tasks.remove(task)  # Remove completed tasks


# # Handler function that will be called whenever a new message is received
# async def on_message(message):
#   print(f"Received message: {message}")
#   # Process the message here as needed

# # Message listener coroutine that will run in the background
# async def message_listener(websocket):
#   while True:
#     message = await websocket.recv()
#     await on_message(message)

# # Main function to connect and initialize the WebSocket connection
# async def receive_messages():
#   async with websockets.connect(
#     "wss://first-response-server-v2-0.onrender.com",
#     subprotocols=["graphql-transport-ws"],
#     extra_headers=[("Cookie", "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzBhMGI1MzNhOTkwN2U2Nzg5ZjJjYTMiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMDk1NzE0MSwiZXhwIjoxNzMxMjE2MzQxfQ.t4gIWDM_dxy1XJenMO6nMPgsLaR-3CBGNt8CE88rYrY; Path=/; Secure; HttpOnly; Expires=Thu, 14 Nov 2024 05:25:41 GMT;")]
#   ) as websocket:
#     # Send connection initialization
#     await websocket.send('{"type": "connection_init"}')
    
#     # Wait for connection acknowledgment
#     while True:
#       message = await websocket.recv()
#       message = json.loads(message)
#       if message["type"] == "connection_ack":
#         print("Connection acknowledged.")
#         break

#     # Send subscription request
#     request = json.dumps({
#       "id": "ad",
#       "type": "subscribe",
#       "payload": {
#         "query": "subscription{sendHello{message}}"
#       }
#     })
#     await websocket.send(request)

#     # Instantiate the event loop and schedule tasks
#     loop = EventLoop()
#     loop.create_task(message_listener(websocket))
#     loop.create_task(main())

#     # Run the event loop
#     loop.run_forever()

# # Example of other tasks to run concurrently with the WebSocket listener
# async def main():
#   while True:
#     print("Performing main tasks...")
#     await sleep(1)


# # Example tasks to run in the event loop
# async def task1():
#   while True:
#     print("Task 1 is running...")
#     await sleep(1)  # Wait 1 second

# async def task2():
#   while True:
#     print("Task 2 is running...")
#     await sleep(2)  # Wait 2 seconds

# import time
# import json
# from websocket import websocket

# # Mock handler function to be called whenever a new message is received
# def on_message(message):
#     print(f"Received message: {message}")
#     # Process the message as needed

# # Main function to initialize the WebSocket connection and listen for messages
# def receive_messages():
#     websocket = websocket_connect("wss://first-response-server-v2-0.onrender.com")
    
#     # Initialize connection
#     init_msg = '{"type": "connection_init"}'
#     websocket.write(init_msg.encode('utf-8'))
    
#     # Wait for connection acknowledgment
#     while True:
#         message = websocket.read()  # Read incoming data
#         if not message:
#             continue
        
#         message = json.loads(message.decode('utf-8'))
#         if message["type"] == "connection_ack":
#             print("Connection acknowledged.")
#             break  # Exit loop when acknowledgment is received

#     # Send subscription request
#     request = {
#         "id": "ad",
#         "type": "subscribe",
#         "payload": {
#             "query": "subscription{sendHello{message}}"
#         }
#     }
#     websocket.write(json.dumps(request).encode('utf-8'))

#     # Main listening loop
#     while True:
#         # Check for new messages
#         message = websocket.read()
#         if message:
#             message = message.decode('utf-8')
#             on_message(message)
        
#         # Sleep briefly to prevent CPU overload
#         time.sleep(0.1)

# # Custom function to simulate async-like connection behavior for the WebSocket
# def websocket_connect(url):
#     # Replace this with actual connection setup logic based on your hardware
#     ws = websocket(url)
#     return ws

# # Run the main function
# receive_messages()