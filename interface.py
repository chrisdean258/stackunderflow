#!/usr/bin/env python3

import requests

url="http://0.0.0.0:5000"

request = requests.post(url + "/newpost", data = { "message" : "hi", "tags": "tags", "sender":"from" })


print(request.text)

