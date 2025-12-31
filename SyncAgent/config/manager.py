import os, yaml
from dotenv import load_dotenv

from SyncAgent.config.schema import AgentConfig

load_dotenv()


class ConfigManager:
    def __init__(self, local_paths, remote_api_endpoint=None, token=None):
        self.local_paths = local_paths
        self.remote_api_endpoint = remote_api_endpoint
        self.token = token

    @staticmethod
    def _load_env():
        return {
            "AGENT_ID": os.getenv("AGENT_ID"),
            "DASHBOARD_URL": os.getenv("DASHBOARD_URL"),
            "DASHBOARD_TOKEN": os.getenv("DASHBOARD_TOKEN"),
            "FTP_PASSWORD": os.getenv("FTP_PASSWORD"),
        }

    @staticmethod
    def _load_yaml(path):
        return yaml.safe_load(open(path)) if os.path.exists(path) else {}

    def _load_local(self):
        config = {}
        for file in self.local_paths:
            config.update(self._load_yaml(file))
        return config


    def _load(self):
        config = {}
        config.update(self._load_local())
        config.update(self._load_env())
        return config

    def build(self) -> AgentConfig:
        data = self._load()  # ← dict آماده
        return AgentConfig(**data)  #