from pydantic import BaseModel


class RsyncItem(BaseModel):
    path: str
    change: str
