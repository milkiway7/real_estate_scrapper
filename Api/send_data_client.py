import httpx

class SendDataClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/analyze"
        self.timeout = httpx.Timeout(15.0)
        self.headers = {
            "Content-Type": "application/json"
            # "Authorization": os.getenv("API_TOKEN")
        }

    async def send_data_to_analysis(self, data):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.base_url, json=data, headers=self.headers)
            response.raise_for_status()
            print("Status:", response.status_code)
            print("Response JSON:", response.json())

