# Three things, http, websocket and json parser
# help('modules')
from utils.connect_wifi import connect_to_wifi
# from utils.urequests import get_request
from utils.urequest import urlopen
import json
connect_to_wifi("iPhone", "Tommy@234")


# get_request("https://phoenixnap.com", 443, "/kb/git-switch-branch")

response = urlopen("https://first-response-server-v2-0.onrender.com", method="GET")

response = json.loads(response)

print(response["message"])
