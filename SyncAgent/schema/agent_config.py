from pathlib import Path

from pydantic import BaseModel, Field, model_validator


class AgentConfig(BaseModel):
    agent_id: str = Field(..., description="Unique ID of this agent instance")

    api_base_url: str
    api_token: str

    ssh_user: str
    ssh_host: str

    push_dir: str
    pull_dir: str
    remote_incoming: str
    remote_outgoing: str

    rsync_path: str = "adapter"
    checksum: bool = False
    min_free_gb: int = 10

    update_config_on_start: bool = True

    @model_validator(mode="after")
    def validate_dir(self):
        if not Path(self.push_dir).resolve().is_dir():
            raise ValueError("push_dir does not exist")
        if not Path(self.pull_dir).is_dir():
            raise ValueError("pull_dir does not exist")

