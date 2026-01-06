import subprocess
import time
from pathlib import Path


class CertificateManager:

    def __init__(
        self,
        ssh_key_path: Path,
        ssh_cert_path: Path,
        min_valid_seconds: int = 3600,
    ):
        self.ssh_key_path = ssh_key_path
        self.ssh_cert_path = ssh_cert_path
        self.min_valid_seconds = min_valid_seconds
        self.ssh_cmd = (
            "ssh "
            f"-i {ssh_key_path} "
            f"-o CertificateFile={ssh_cert_path} "
            "-o IdentitiesOnly=yes "
            "-o BatchMode=yes "
            "-o StrictHostKeyChecking=yes "
            "-o ServerAliveInterval=30 "
            "-o ServerAliveCountMax=5 "
            "-o Compression=no"
        )

    def ensure_valid_certificate(self):
        if not self.cert_path.exists():
            self._obtain_certificate()
            return

        if self._seconds_until_expiry() < self.min_valid_seconds:
            self._obtain_certificate()

    def _seconds_until_expiry(self) -> int:
        proc = subprocess.run(
            ["ssh-keygen", "-L", "-f", str(self.cert_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if proc.returncode != 0:
            return 0

        for line in proc.stdout.splitlines():
            if "Valid:" in line and "to" in line:
                # Example: Valid: from 2026-01-06T06:00:00 to 2026-01-07T06:00:00
                expiry = line.split("to")[1].strip()
                expiry_ts = time.mktime(
                    time.strptime(expiry, "%Y-%m-%dT%H:%M:%S")
                )
                return int(expiry_ts - time.time())

        return 0

    def _obtain_certificate(self):
        """
        این متد باید به CA واقعی وصل شود.
        اینجا فرض می‌کنیم step-ca CLI وجود دارد.
        """
        cmd = [
            "step",
            "ssh",
            "certificate",
            "--force",
            "sync-agent",
            str(self.key_path),
            str(self.cert_path),
        ]

        proc = subprocess.run(cmd)
        if proc.returncode != 0:
            raise RuntimeError("Failed to obtain SSH certificate")
