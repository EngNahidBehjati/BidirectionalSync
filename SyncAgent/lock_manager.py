import json
import os
import socket
import time
from pathlib import Path
from datetime import datetime


class LockError(Exception):
    pass


class LockManager:

    def __init__(self, lock_path: Path):
        self.lock_path = lock_path
        self.lock_start_time = None

    def __enter__(self):
        self.acquire(run_id="pending")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self, run_id: str):
        if self.lock_path.exists():
            if self._is_active_lock():
                raise LockError("another sync-agent run is active")
            self._reclaim()

        self._write_lock(run_id)

    def release(self):
        try:
            if self.lock_path.exists():
                self.lock_path.unlink()
        except Exception as e:
            #todo Log Exception
            return

    def _is_active_lock(self) -> bool:
        try:
            data = json.loads(self.lock_path.read_text())
            pid = data.get("pid")
            if not pid:
                return False
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except Exception:
            return False

    def _reclaim(self):
        backup = self.lock_path.with_suffix(f".stale.{int(time.time())}")
        self.lock_path.rename(backup)

    def _write_lock(self, run_id: str):
        self.lock_start_time = datetime.utcnow().isoformat() + "Z"
        data = {
            "pid": os.getpid(),
            "start_time": self.lock_start_time,
            "hostname": socket.gethostname(),
            "run_id": run_id,
        }

        tmp = self.lock_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        tmp.replace(self.lock_path)
