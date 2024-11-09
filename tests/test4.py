import socket
import os
import json
import time
from utils.ubinascii import b2a_base64, hexlify
from utils.connect_wifi import connect_to_wifi

class EventLoop:
  def __init__(self):
    self.queue = []

  def create_task(self, coro):
    self.queue.append(coro)

  def run_until_complete(self):
    while self.queue:
      task = self.queue.pop(0)
      try:
        # Run until the next yield
        next(task)
        # If yielded, re-add to queue to continue processing later
        self.queue.append(task)
      except StopIteration:
        # Task complete, do nothing
        pass


def read(socket):
  str = b""
  while True:
    l = socket.readline()
    if not l or l == b"\r\n":
      break
    str += l
  return str

def send_ping(socket):
  # Create a WebSocket ping frame with a mask
  ping_frame = bytearray([0x89])  # 0x89 (FIN + ping opcode)

  # Ping frame has no payload, so payload length is zero
  payload_length = 0
  ping_frame.append(0x80 | payload_length)  # Mask bit set and length 0

  # Generate a 4-byte masking key
  masking_key = os.urandom(4)
  ping_frame.extend(masking_key)  # Append the masking key to the frame

  # Send the masked ping frame
  socket.write(ping_frame)

def send_pong(socket):
  # Create a WebSocket pong frame with a mask
  pong_frame = bytearray([0x8A])  # 0x8A (FIN + pong opcode)

  # Pong frame has no payload, so payload length is zero
  payload_length = 0
  pong_frame.append(0x80 | payload_length)  # Mask bit set and length 0

  # Generate a 4-byte masking key
  masking_key = os.urandom(4)
  pong_frame.extend(masking_key)  # Append the masking key to the frame

  # Send the masked pong frame
  socket.write(pong_frame)

def send_websocket_message(socket, message):
  # Create a WebSocket frame for a text message
  frame = bytearray()

  # Set FIN bit and text frame opcode
  frame.append(0x81)  # 0x80 (FIN) | 0x1 (text)

  # Determine the payload length and set accordingly
  payload_length = len(message)
  if payload_length <= 125:
    frame.append(0x80 | payload_length)  # 0x80 indicates masking
  elif payload_length <= 65535:
    frame.append(0xFE)
    frame.extend(payload_length.to_bytes(2, 'big'))
  else:
    frame.append(0xFF)
    frame.extend(payload_length.to_bytes(8, 'big'))

  # Generate a masking key and mask the payload
  masking_key = os.urandom(4)
  frame.extend(masking_key)

  # Apply mask to the payload
  masked_payload = bytearray([message[i] ^ masking_key[i % 4] for i in range(payload_length)])
  frame.extend(masked_payload)

  # Send the framed message
  socket.write(frame)

# def receive_websocket_message(socket):
#   # Read the first byte for FIN and opcode
#   first_byte = socket.read(1)
#   if not first_byte:
#     return None
#   fin_and_opcode = ord(first_byte)

#   # Read the payload length
#   second_byte = ord(socket.read(1))
#   masked = (second_byte & 0x80) != 0
#   payload_length = second_byte & 0x7F

#   if payload_length == 126:
#     payload_length = int.from_bytes(socket.read(2), 'big')
#   elif payload_length == 127:
#     payload_length = int.from_bytes(socket.read(8), 'big')

#   # Read the masking key if present
#   if masked:
#     masking_key = socket.read(4)
#   else:
#     masking_key = None

#   # Read the payload data
#   payload = socket.read(payload_length)
#   if masked:
#     payload = bytearray([payload[i] ^ masking_key[i % 4] for i in range(payload_length)])

#   print(payload)
#   return payload.decode('utf-8')

def receive_websocket_message(socket):
    # Read the first byte for FIN and opcode
    first_byte = socket.read(1)
    if not first_byte:
      return None
    fin_and_opcode = ord(first_byte)
    
    # Extract the opcode
    opcode = fin_and_opcode & 0x0F
    print(fin_and_opcode, opcode)
    if(opcode == 0x0):
      return None
    # 0x1 = Text frame, 0x2 = Binary frame, 0x9 = Ping, 0xA = Pong
    # send_pong(socket)
    if opcode == 0x8:
      print("Received close frame;")
      # Respond to close with close frame
      # close_frame = bytearray([0x88, 0x00])  # 0x88 is a close frame with no payload
      # socket.write(close_frame)
      return None
    elif opcode == 0x9:
      print("Received ping frame; responding with pong")
      # Respond to ping with pong
      # pong_frame = bytearray([0x8A, 0x00])  # 0x8A is a pong frame with no payload
      # socket.write(pong_frame)
      send_pong(socket)
      return None
    elif opcode == 0xA:
      print("Received pong frame")
      return None

    # Read the payload length
    second_byte = ord(socket.read(1))
    masked = (second_byte & 0x80) != 0
    payload_length = second_byte & 0x7F

    if payload_length == 126:
        payload_length = int.from_bytes(socket.read(2), 'big')
    elif payload_length == 127:
        payload_length = int.from_bytes(socket.read(8), 'big')

    # Read the masking key if present
    if masked:
        masking_key = socket.read(4)
    else:
        masking_key = None

    # Read the payload data
    payload = socket.read(payload_length)
    if masked:
        payload = bytearray([payload[i] ^ masking_key[i % 4] for i in range(payload_length)])

    # Decode only if it's a text frame
    if opcode == 0x1:  # Text frame
        return payload.decode('utf-8')
    else:  # Other opcodes like Binary frame
        return payload  # Return as raw data without decoding

# def receive_websocket_message(socket):
#     # Read the first byte for FIN and opcode
#     first_byte = socket.read(1)
#     if not first_byte:
#         return None
#     fin_and_opcode = ord(first_byte)
    
#     # Extract the opcode
#     opcode = fin_and_opcode & 0x0F
#     # Handle control frames (close, ping, pong)
#     if opcode == 0x8:
#         print("Received close frame")
#         return None
#     elif opcode == 0x9:
#         print("Received ping frame; sending pong")
#         send_pong(socket)
#         return None
#     elif opcode == 0xA:
#         print("Received pong frame")
#         return None

#     # Read the payload length and masking
#     second_byte = ord(socket.read(1))
#     masked = (second_byte & 0x80) != 0
#     payload_length = second_byte & 0x7F

#     if payload_length == 126:
#         payload_length = int.from_bytes(socket.read(2), 'big')
#     elif payload_length == 127:
#         payload_length = int.from_bytes(socket.read(8), 'big')

#     # Read the masking key if present
#     masking_key = socket.read(4) if masked else None

#     # Read the payload data
#     payload = socket.read(payload_length)
#     if masked:
#         # Unmask payload if needed
#         payload = bytearray([payload[i] ^ masking_key[i % 4] for i in range(payload_length)])

#     # Decode text frame payload
#     if opcode == 0x1:  # Text frame
#         return payload.decode('utf-8')
#     else:  # Binary frame or others
#         return payload



def connect_websocket_with_headers(url, headers=None, subprotocols=None):
  try:
    proto, dummy, host, path = url.split("/", 3)
  except ValueError:
    proto, dummy, host = url.split("/", 2)
    path = ""

  if proto == "ws:":
    port = 80
  elif proto == "wss:":
    import tls

    port = 443
  else:
    raise ValueError("Unsupported protocol: " + proto)

  if ":" in host:
    host, port = host.split(":", 1)
    port = int(port)

  ai = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
  ai = ai[0]

  s = socket.socket(ai[0], ai[1], ai[2])
  try:
    s.connect(ai[-1])
    if proto == "wss:":
      context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
      context.verify_mode = tls.CERT_NONE
      s = context.wrap_socket(s, server_hostname=host)


    sec_websocket_key = b2a_base64(os.urandom(16)).strip()

    # Create the HTTP GET request message
    headers_list = [
      f"GET /{path} HTTP/1.1",
      f"Host: {host}",
      "Upgrade: websocket",
      "Connection: Upgrade",
      f"Sec-WebSocket-Key: {sec_websocket_key}",
      "Sec-WebSocket-Version: 13"
    ]

    # Add any custom headers
    if headers:
      for key, value in headers.items():
        headers_list.append(f"{key}: {value}")

    # Add the subprotocols header if specified
    if subprotocols:
      headers_list.append(f"Sec-WebSocket-Protocol: {', '.join(subprotocols)}")

    handshake = "\r\n".join(headers_list) + "\r\n\r\n"

    print(handshake)
    s.write(handshake.encode())
    print("Complete data received:", read(s))
  except OSError:
    s.close()
    raise

  print("Reading response")
  return s

wlan = connect_to_wifi("IIT-IoT", "IPRO-POE-ESP-32-1")

# Usage example with headers and subprotocols
# url = "wss://echo.websocket.org/tomiwa"
url = "wss://first-response-server-v2-0.onrender.com"
headers = {
  "Cookie": "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzBhMGI1MzNhOTkwN2U2Nzg5ZjJjYTMiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMDk1NzE0MSwiZXhwIjoxNzMxMjE2MzQxfQ.t4gIWDM_dxy1XJenMO6nMPgsLaR-3CBGNt8CE88rYrY; Path=/; Secure; HttpOnly; Expires=Thu, 14 Nov 2024 05:25:41 GMT;",
}
subprotocols = ["graphql-transport-ws"]

s = connect_websocket_with_headers(url, headers, subprotocols)

message = {
  "type": "connection_init"
}
message = json.dumps(message).encode('utf-8')
send_websocket_message(s, message)
# time.sleep(2)
print("Complete data received:", receive_websocket_message(s))

message = {
  "id": "ad",
  "type": "subscribe",
  "payload": {
    "query": "subscription{sendHello{message}}"
  }
}
message = json.dumps(message).encode('utf-8')

send_websocket_message(s, message)

print(help(s))


# Keep connection alive with periodic pings
try:
  while True:
    # send_ping(s)  # Send ping to keep the connection alive
    # send_pong(s)
    print("Ping sent to keep connection alive")
    response = receive_websocket_message(s)
    if response:
      print("Message from server:", response)
    time.sleep(3)  # Wait for 3 seconds (adjust as needed)
except KeyboardInterrupt:
  print("Closing connection")
except OSError as err:
  print(err)
  print("Connection closed")
finally:
  s.close()