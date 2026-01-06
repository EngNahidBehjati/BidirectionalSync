from pydantic import BaseModel


class Metadata(BaseModel):
    path: str
    size: int
    mtime: int
    checksum: str | bool