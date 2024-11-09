from my_module.ubinascii import hexlify
from my_module.connect_wifi import connect_to_wifi

def get_mac_address(SSID, PASSWORD):
  wlan = connect_to_wifi(SSID, PASSWORD)
  mac = hexlify(wlan.config('mac'))
  return mac.decode()