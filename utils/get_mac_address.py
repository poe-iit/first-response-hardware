from utils.ubinascii import hexlify
from utils.connect_wifi import connect_to_wifi

def get_mac_address(wlan):
  mac = hexlify(wlan.config('mac'))
  return mac.decode()