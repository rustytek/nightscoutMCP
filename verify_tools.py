import os
import json
import sys
from dotenv import load_dotenv
from nightscout import NightscoutClient
import analysis

# Load environment variables
load_dotenv()

url = os.getenv("NIGHTSCOUT_URL")
api_secret = os.getenv("API_SECRET")

if not url:
    print("Error: NIGHTSCOUT_URL not found in .env")
    sys.exit(1)

print(f"Connecting to Nightscout at: {url}")
client = NightscoutClient(url, api_secret)

print("\n--- Testing Suggest Settings Tool Logic ---")
try:
    # 1. Fetch Data
    print("Fetching last 24h data (approx 288 entries)...")
    entries = client.get_entries(count=288)
    treatments = client.get_treatments(count=288)
    device_statuses = client.get_device_status(count=288)
    profile = client.get_profile()
    
    print(f"Fetched {len(entries)} entries and {len(device_statuses)} device statuses.")
    
    # 2. Run Analysis
    print("Running analysis...")
    suggestions = analysis.analyze_settings(profile, entries, treatments, device_statuses)
    
    # 3. Print Results
    print("\nSuggestions:")
    print(json.dumps(suggestions, indent=2))
    
    if len(entries) > 0:
        stats = analysis.calculate_statistics(entries)
        print("\nStatistics Debug:")
        print(json.dumps(stats, indent=2))

except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)
