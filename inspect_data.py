import os
import json
import sys
from dotenv import load_dotenv
from nightscout import NightscoutClient

load_dotenv()
client = NightscoutClient(os.getenv("NIGHTSCOUT_URL"), os.getenv("API_SECRET"))

try:
    print("Fetching latest device status...")
    status = client.get_device_status(count=1)
    if status:
        print("Top level keys:", list(status[0].keys()))
        if 'loop' in status[0]:
             print("\n'loop' keys:", list(status[0]['loop'].keys()))
             print("\nSample 'loop' data:", json.dumps(status[0]['loop'], indent=2))
        if 'openaps' in status[0]:
             print("\n'openaps' keys:", list(status[0]['openaps'].keys()))
    else:
        print("No device status found.")

except Exception as e:
    print(e)
