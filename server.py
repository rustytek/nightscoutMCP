import os
import json
import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from nightscout import NightscoutClient

# Load environment variables
load_dotenv()

NIGHTSCOUT_URL = os.getenv("NIGHTSCOUT_URL")
API_SECRET = os.getenv("API_SECRET")

if not NIGHTSCOUT_URL:
    raise ValueError("NIGHTSCOUT_URL environment variable is not set")

# Initialize Nightscout Client
client = NightscoutClient(NIGHTSCOUT_URL, API_SECRET)

# Initialize MCP Server
mcp = FastMCP("Nightscout")

@mcp.resource("nightscout://entries")
def get_entries() -> str:
    """Get the latest glucose entries from Nightscout."""
    entries = client.get_entries(count=10)
    return json.dumps(entries, indent=2)

@mcp.resource("nightscout://treatments")
def get_treatments() -> str:
    """Get the latest treatments from Nightscout."""
    treatments = client.get_treatments(count=10)
    return json.dumps(treatments, indent=2)

@mcp.resource("nightscout://profile")
def get_profile() -> str:
    """Get the active Nightscout profile."""
    profile = client.get_profile()
    return json.dumps(profile, indent=2)

@mcp.resource("nightscout://device_status")
def get_device_status() -> str:
    """Get the latest device status."""
    status = client.get_device_status(count=1)
    return json.dumps(status, indent=2)

@mcp.tool()
def suggest_settings(hours: int = 24) -> str:
    """
    Analyze Nightscout data and suggest therapy setting changes.
    
    Args:
        hours: Number of hours of data to analyze (default: 24).
    """
    # Estimate count: 12 entries per hour
    count = hours * 12
    
    # Fetch data
    try:
        entries = client.get_entries(count=count)
        treatments = client.get_treatments(count=count)
        # Fetch device status for the same period
        device_statuses = client.get_device_status(count=count)
        profile = client.get_profile()
    except Exception as e:
        return f"Error fetching data from Nightscout: {str(e)}"

    # Run Analysis
    import analysis
    suggestions = analysis.analyze_settings(profile, entries, treatments, device_statuses)
    
    return json.dumps(suggestions, indent=2)

if __name__ == "__main__":
    mcp.run()
