import requests

from config.schema import AgentConfig
from interface_ports.remote_port import IRemotePort


class HTTPServerAdaptor(IRemotePort):
    def __init__(self, config: AgentConfig):
        self._base_url = config.remote_path.rstrip('/')
        self._token = config.token
        self._headers = {"Authorization": f"Token {self._token}"}

        self._heartbeat_api = f"{self._base_url}/heartbeat/"
        self._config_api = f"{self._base_url}/config/"
        self._run_status_api = f"{self._base_url}/runs/"


    def heartbeat(self):
        return requests.get(self._heartbeat_api, headers=self._headers)

    def fetch_remote_config(self):
        return requests.get(self._config_api, headers=self._headers)

    def send_run_status(self, payload):
        return requests.post(self._run_status_api, json=payload, headers=self._headers)
