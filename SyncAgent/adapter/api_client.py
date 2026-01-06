import requests


class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: dict):
        r = requests.post(
            self.base + path,
            json=payload,
            headers=self.headers,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def patch(self, path: str, payload: dict):
        r = requests.patch(
            self.base + path,
            json=payload,
            headers=self.headers,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
