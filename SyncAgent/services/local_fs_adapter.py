from pathlib import Path
import hashlib

import shutil
import time


class LocalFSAdapter:
    def __init__(self, base_dir: str):
        self.base = Path(base_dir).resolve()

    def _resolve(self, relative_path: str) -> Path:
        full = (self.base / relative_path).resolve()
        if not str(full).startswith(str(self.base)):
            raise PermissionError("Path traversal detected")
        return full

    def list_agent(self) -> set[str]:
        files = set()
        for path in self.base.rglob("*"):
            if path.is_file():
                files.add(str(path.relative_to(self.base)))
        return files


    def stat_agent(self, file: str):
        path = self._resolve(file)
        stat = path.stat()

        return {
            "type": "file",
            "modified": stat.st_mtime,
            "size": stat.st_size,
            "checksum": self._checksum(path),
            "metadata": {
                "mode": stat.st_mode,
            }
        }

    def _checksum(self, path: Path):
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def write_agent(self, file: str, content: bytes):
        path = self._resolve(file)
        path.parent.mkdir(parents=True, exist_ok=True)

        tmp = path.with_suffix(".tmp")
        with tmp.open("wb") as f:
            f.write(content)

        tmp.replace(path)

    def delete_agent(self, file: str):
        path = self._resolve(file)
        if path.exists():
            path.unlink()


    def backup_agent(self, file: str):
        path = self._resolve(file)
        if not path.exists():
            return

        backup_name = f"{path.name}.bak.{int(time.time())}"
        backup_path = path.with_name(backup_name)

        shutil.move(str(path), str(backup_path))


