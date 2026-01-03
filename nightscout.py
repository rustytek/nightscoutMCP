import os
import hashlib
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime

class NightscoutClient:
    def __init__(self, url: str, api_secret: Optional[str] = None):
        self.url = url.rstrip('/')
        self.api_secret = api_secret
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if api_secret:
            # Nightscout accepts SHA1 hash of the API secret in the 'api-secret' header
            self.headers['api-secret'] = hashlib.sha1(api_secret.encode('utf-8')).hexdigest()

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        try:
            response = requests.get(f"{self.url}/api/v1/{endpoint}", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Nightscout: {e}")
            raise

    def get_entries(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest glucose entries."""
        return self._get('entries.json', params={'count': count})

    def get_treatments(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get latest treatments (bolus, carb, temp basal)."""
        return self._get('treatments.json', params={'count': count})

    def get_profile(self) -> Dict[str, Any]:
        """Get the active profile."""
        # Profile endpoint often returns a list, usually we want the first/active one
        return self._get('profile.json')

    def get_device_status(self, count: int = 1) -> List[Dict[str, Any]]:
        """Get device status (pump battery, loop status)."""
        return self._get('devicestatus.json', params={'count': count})
