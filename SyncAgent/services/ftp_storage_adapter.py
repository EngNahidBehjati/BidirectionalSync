from ftplib import FTP
from pathlib import PurePosixPath
import hashlib
import io

class FTPStorageAdapter:
    def __init__(self, host, user, password, base_dir):
        self.ftp = FTP(host)
        self.ftp.login(user=user, passwd=password)
        self.base = PurePosixPath(base_dir)

    def _remote_path(self, relative_path: str) -> str:
        path = self.base / relative_path
        return str(path)

    def list_superior(self) -> set[str]:
        files = set()

        def walker(line):
            parts = line.split()
            name = parts[-1]
            if not name.startswith("."):
                files.add(name)

        self.ftp.cwd(str(self.base))
        self.ftp.retrlines("NLST", walker)

        return files

    def stat_superior(self, file: str):
        path = self._remote_path(file)
        size = self.ftp.size(path)

        modified = self._get_mtime(path)
        checksum = self._checksum(path)

        return {
            "type": "file",
            "size": size,
            "modified": modified,
            "checksum": checksum,
            "metadata": {}
        }

    def _get_mtime(self, path: str):
        resp = self.ftp.sendcmd(f"MDTM {path}")
        return resp[4:]  # YYYYMMDDHHMMSS

    def _checksum(self, path: str):
        h = hashlib.sha256()

        def reader(chunk):
            h.update(chunk)

        self.ftp.retrbinary(f"RETR {path}", reader)
        return h.hexdigest()

    def read_superior(self, file: str) -> bytes:
        path = self._remote_path(file)
        buf = io.BytesIO()
        self.ftp.retrbinary(f"RETR {path}", buf.write)
        return buf.getvalue()
