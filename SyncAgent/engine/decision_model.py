from pydantic import BaseModel
from typing import Literal
## TODO remove
class SyncAction(BaseModel):
    type: Literal[
        "PULL", "PUSH",
        "DELETE_LOCAL",
        "UPDATE_LOCAL", "UPDATE_REMOTE",
        "CONFLICT"
    ]
    file: str
    reason: str | None = None
    local_ts: float | None = None  # timestamp local
    remote_ts: float | None = None # timestamp remote