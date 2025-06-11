import httpx
from Helpers.logger import get_logger

class SendDataClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/analyze"
        self.timeout = httpx.Timeout(15.0)
        self.headers = {"Content-Type": "application/json"}
        self.logger = get_logger(self.__class__.__name__)

    async def send_data_to_analysis(self, data):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(self.base_url, json=data, headers=self.headers)
                response.raise_for_status()
                self.logger.info(f"Data sent successfully to the analysis endpoint. Status code: {response.status_code}")
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")


