import requests
from src.utils.exceptions import N8NCommunicationError

class N8NClient:
    def __init__(self, webhook_url):
        self.url = webhook_url

    def send_payload(self, data: dict) -> dict:
        try:
            response = requests.post(self.url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise N8NCommunicationError(f"N8N Request Failed: {str(e)}")