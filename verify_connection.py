import os
import sys
from dotenv import load_dotenv
from nightscout import NightscoutClient

# Load environment variables
load_dotenv()

url = os.getenv("NIGHTSCOUT_URL")
api_secret = os.getenv("API_SECRET")

if not url:
    print("Error: NIGHTSCOUT_URL not found in .env")
    sys.exit(1)

print(f"Connecting to Nightscout at: {url}")
client = NightscoutClient(url, api_secret)

try:
    print("Fetching entries...")
    entries = client.get_entries(count=1)
    print(f"Success! Retrieved {len(entries)} entry.")
    
    print("Fetching profile...")
    profile = client.get_profile()
    print("Success! Retrieved profile.")
    
    print("Connection verification successful.")
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
