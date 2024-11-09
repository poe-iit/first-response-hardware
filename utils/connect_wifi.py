import network
import time

def connect_to_wifi(SSID = 'iPhone', PASSWORD = 'Tommy@234'):
  # Initialize the station interface
  wifi = network.WLAN(network.STA_IF)

  # Activate the station interface
  wifi.active(True)

  # Connect to the Wi-Fi network
  wifi.connect(SSID, PASSWORD)

  # Wait until connected
  print("Connecting to Wi-Fi...")
  while not wifi.isconnected():
      time.sleep(1)

  # Display the connection details
  print("Connected to Wi-Fi!")
  print("Network config:", wifi.ifconfig())
  return wifi