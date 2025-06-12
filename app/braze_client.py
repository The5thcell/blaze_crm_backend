import httpx
import asyncio

class BrazeClient:
    BASE_URL = "https://rest.iad-01.braze.com"
    MAX_RETRIES = 3

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10)

    async def send_event(self, payload: dict) -> bool:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = f"{self.BASE_URL}/messages/send"
        for attempt in range(self.MAX_RETRIES):
            try:
                response = await self.client.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    return True
                elif response.status_code in (429, 503):  # rate limit or service unavailable
                    await asyncio.sleep(2 ** attempt)  # exponential backoff
                else:
                    response.raise_for_status()
            except httpx.HTTPError as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(2 ** attempt)
        return False