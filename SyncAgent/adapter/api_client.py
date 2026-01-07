import socket
import uuid

import requests


class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _post(self, path: str, payload: dict):
        r = requests.post(
            self.base + path,
            json=payload,
            headers=self.headers,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def _patch(self, path: str, payload: dict):
        r = requests.patch(
            self.base + path,
            json=payload,
            headers=self.headers,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def get_run(self, agent_id: str, lock_start_time: int):
        idempotency_key = f"{agent_id}:{lock_start_time}"
        payload = {
            "agent_id": agent_id,
            "hostname": socket.gethostname(),
            "idempotency_key": idempotency_key,
        }
        resp = self._post("/runs/register", payload)
        run_id = resp.get("run_id", None)
        if run_id is None:
            raise ValueError("Not a valid run_id")
        return run_id