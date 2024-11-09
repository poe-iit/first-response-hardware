import socket
import ssl
import tls

print(help(tls))
print(help(ssl))

def get_request(host, port, path="/", **kwargs):
  # Create a socket object
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to the host
  s.connect((host, port))

  # Wrap the socket with SSL
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  context.verify_mode = ssl.CERT_NONE
  s = context.wrap_socket(s, server_hostname=host)

  # Create the HTTP GET request message
  request = "GET %s HTTP/1.1\r\n" % path
  request += "Host: %s\r\n" % host
  request += "Connection: close\r\n\r\n"

  print(request)
  print(request.encode())

  print(help(s))
  # Send the HTTP request using the ssl_socket
  s.write(request.encode())  # Fix: use ssl_socket instead of s

  # Receive the response
  response = s.read(4096)  # Fix: use ssl_socket to receive data

  # Print the response
  print(response)
  print(response.decode())

  # Close the SSL socket
  s.close()

  # Return the response
  return response