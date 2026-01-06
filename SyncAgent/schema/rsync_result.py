from pydantic import BaseModel


class RsyncResult(BaseModel):
        code: int
        stdout: str
        stderr: str

