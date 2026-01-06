import os

from schema.agent_config import AgentConfig
from dotenv import load_dotenv


load_dotenv(
    dotenv_path="../.env",
)
class ConfigManager:
    @staticmethod
    def _load_env():
        data = {"agent_id" : os.getenv("AGENT_ID"),
                "api_base_url": os.getenv("API_BASE_URL"),
                "api_token": os.getenv("API_TOKEN"),
                "ssh_user" :os.getenv("SSH_USER"),
                "ssh_host": os.getenv("SSH_HOST"),
                "push_dir" :os.getenv("PUSH_DIR"),
                "pull_dir" :os.getenv("PULL_DIR"),
                "remote_incoming" :os.getenv("REMOTE_INCOMING"),
                "remote_outgoing" :os.getenv("REMOTE_OUTGOING"),
                "rsync_path": os.getenv("RSYNC_PATH", "adapter"),
                "checksum": os.getenv("CHECKSUM", False),
                "min_free_gb" :os.getenv("MIN_FREE_GB", 10),
                "update_config_on_start": os.getenv("UPDATE_CONFIG_ON_START", True)}
        return data

    def build(self) -> AgentConfig:
        data = self._load_env()
        return AgentConfig(**data)  #