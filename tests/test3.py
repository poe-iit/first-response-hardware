import socket
import os
from utils.ubinascii import b2a_base64
from utils.connect_wifi import connect_to_wifi
from utils.urequest import urlopen
import websocket
import time

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

def connect_websocket_with_headers(url, headers=None, subprotocols=None):
  print(1)
  try:
    proto, dummy, host, path = url.split("/", 3)
  except ValueError:
    proto, dummy, host = url.split("/", 2)
    path = ""

  print(2)
  if proto == "ws:":
    port = 80
  elif proto == "wss:":
    import tls

    port = 443
  else:
    raise ValueError("Unsupported protocol: " + proto)

  print(3)
  if ":" in host:
    host, port = host.split(":", 1)
    port = int(port)

  print(host, port)
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
    l = s.readline()
    while True:
      l = s.readline()
      if not l or l == b"\r\n":
        break
      if l.startswith(b"Transfer-Encoding:"):
        if b"chunked" in l:
          raise ValueError("Unsupported " + l)
      elif l.startswith(b"Location:"):
        raise NotImplementedError("Redirects not yet supported")
  except OSError:
    s.close()
    raise

  print("Reading response")
  
  ws = websocket.websocket(s)
  print(help(s))
  return ws, s












    # # Parse the WebSocket URL
    # _, _, host, path = url.split("/", 3)
    # port = 443 if url.startswith("wss") else 80
    # print(host, port)
    # ai = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1]
    
    # # Establish a socket connection
    # sock = socket.socket()
    # sock.connect(addr)
    
    # # Build WebSocket upgrade headers
    # handshake = (
    #     "GET /{} HTTP/1.1\r\n"
    #     "Host: {}\r\n"
    #     "Upgrade: websocket\r\n"
    #     "Connection: Upgrade\r\n"
    #     "Sec-WebSocket-Key: {}\r\n"
    #     "Sec-WebSocket-Version: 13\r\n"
    # ).format(path, host, b2a_base64(os.urandom(16)).strip())
    
    # # Add any custom headers
    # if headers:
    #     for key, value in headers.items():
    #         handshake += "{}: {}\r\n".format(key, value)
    
    # # Add the subprotocols header if specified
    # if subprotocols:
    #     handshake += "Sec-WebSocket-Protocol: {}\r\n".format(", ".join(subprotocols))
    
    # handshake += "\r\n"
    
    # # Send the WebSocket handshake request
    # sock.send(handshake.encode())
    
    # # Read response from server
    # response = sock.recv(1024)
    # if b" 101 " not in response:
    #     raise ConnectionError("WebSocket handshake failed")
    
    # # Wrap the socket in the websocket object
    # ws = websocket.websocket(sock)
    # return ws

connect_to_wifi("iPhone", "Tommy@234")

# Usage example with headers and subprotocols
url = "wss://echo.websocket.org/tomiwa"
# url = "wss://://first-response-server-v2-0.onrender.com"
headers = {
  "Cookie": "sessionId=12345",
}
subprotocols = ["graphql-transport-ws"]

# print(urlopen(url))
# loop = EventLoop()
# loop.create_task(connect_websocket_with_headers("wss://echo.websocket.org"))
# loop.run_until_complete()
ws, s = connect_websocket_with_headers(url)
# ws = connect_websocket_with_headers(url, headers, subprotocols)

# # Example of sending and receiving messages
print(help(ws), help(s))
print("Got here")

message = b"Hello, WebSocket!\r\n\r\n"
s.write(message)  # Send message
# time.sleep(2)
l = s.readline()
print(l)
while True:
  l = s.readline()
  print(l)
  if not l or l == b"\r\n":
    break
  if l.startswith(b"Transfer-Encoding:"):
    if b"chunked" in l:
      raise ValueError("Unsupported " + l)
  elif l.startswith(b"Location:"):
    raise NotImplementedError("Redirects not yet supported")
buffer = bytearray()
while True:
  chunk = ws.read(32)  # Read in chunks of 32 bytes
  if not chunk:
    break  # No more data
  buffer.extend(chunk)
print("Complete data received:", buffer)

s.write(message)  # Send message
# time.sleep(2)
buffer = bytearray()
while True:
  chunk = ws.read(32)  # Read in chunks of 32 bytes
  if not chunk:
    break  # No more data
  buffer.extend(chunk)
print("Complete data received:", buffer)
l = s.readline()
print(l)
while True:
  l = s.readline()
  print(l)
  if not l or l == b"\r\n":
    break
  if l.startswith(b"Transfer-Encoding:"):
    if b"chunked" in l:
      raise ValueError("Unsupported " + l)
  elif l.startswith(b"Location:"):
    raise NotImplementedError("Redirects not yet supported")
  

s.write(message)  # Send message
# time.sleep(2)
buffer = bytearray()
while True:
  chunk = ws.read(32)  # Read in chunks of 32 bytes
  if not chunk:
    break  # No more data
  buffer.extend(chunk)
print("Complete data received:", buffer)
l = s.readline()
print(l)
while True:
  l = s.readline()
  print(l)
  if not l or l == b"\r\n":
    break
  if l.startswith(b"Transfer-Encoding:"):
    if b"chunked" in l:
      raise ValueError("Unsupported " + l)
  elif l.startswith(b"Location:"):
    raise NotImplementedError("Redirects not yet supported")


# buffer = bytearray(64)  # Create a buffer of 64 bytes
# bytes_read = ws.readinto(buffer)
# print("Received data:", buffer[:bytes_read])  # Print only the received portion
# Receive a response
# l = ws.readline(1024)
# while l:
#   print(l)
#   l = ws.readline(1024)
#   print(l)

# # Always remember to close the WebSocket when done


ws.close()