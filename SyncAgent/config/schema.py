from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    agent_id: str = Field(..., description="Unique ID of this agent instance")

    dashboard_url: str
    dashboard_token: str

    ftp_host: str
    ftp_user: str
    ftp_pass: str

    local_path: str
    remote_path: str

    update_config_on_start: bool = True
