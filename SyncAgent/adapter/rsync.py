import subprocess
import hashlib
from pathlib import Path

from typing import List

from enums.sync_status import SyncStatus
from schema.metadata import Metadata
from schema.rsync_item import RsyncItem
from schema.rsync_result import RsyncResult


class Rsync:
    success_code = 0
    partial_code = (23, 24)
    @staticmethod
    def run_rsync(cmd: List[str]) -> RsyncResult:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return RsyncResult(code=proc.returncode,
                           stdout=proc.stdout,
                           stderr=proc.stderr)

    @staticmethod
    def parse_rsync_output(stdout: str) -> List[RsyncItem]:
        items = []
        for line in stdout.splitlines():
            if not line.strip():
                continue
            change, path = line.split(" ", 1)
            items.append(RsyncItem(path=path, change=change))
        return items

    @classmethod
    def classify_exit_code(cls, code: int) -> SyncStatus:
        if code == cls.success_code:
            return SyncStatus.Success
        if code in cls.partial_code:
            return SyncStatus.Partial
        return SyncStatus.Failed

    @staticmethod
    def file_metadata(path: Path, checksum: bool = False) -> Metadata:
        stat = path.stat()
        if checksum:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            checksum = h.hexdigest()
        meta = Metadata(
            path=str(path),
            size=stat.st_size,
            mtime=int(stat.st_mtime),
            checksum=checksum,
        )

        return meta

