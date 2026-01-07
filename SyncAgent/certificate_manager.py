import subprocess
import time
from pathlib import Path


class CertificateError(Exception):
    pass


class CertificateManager:
    def __init__(
        self,
        key_path: Path,
        cert_path: Path,
        ca_url: str,
        principal: str,
        ca_fingerprint_path: Path,
        min_valid_seconds: int = 3600,
    ):
        self.key_path = key_path
        self.cert_path = cert_path
        self.ca_url = ca_url
        self.principal = principal
        self.ca_fingerprint_path = ca_fingerprint_path
        self.min_valid_seconds = min_valid_seconds

    def ensure(self):
        self._ensure_keypair()

        if not self.cert_path.exists():
            self._issue()
            return

        if self._seconds_until_expiry() < self.min_valid_seconds:
            self._issue()

    def _ensure_keypair(self):
        if self.key_path.exists():
            return

        cmd = [
            "ssh-keygen",
            "-t", "ed25519",
            "-f", str(self.key_path),
            "-N", "",
        ]
        self._run(cmd, "failed to generate agent ssh key")

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
                expiry = line.split("to")[1].strip()
                expiry_ts = time.mktime(
                    time.strptime(expiry, "%Y-%m-%dT%H:%M:%S")
                )
                return int(expiry_ts - time.time())

        return 0

    def _issue(self):
        fingerprint = self._get_ca_fingerprint()

        cmd = [
            "step", "ssh", "certificate",
            self.principal,
            str(self.key_path),
            str(self.cert_path),
            "--ca-url", self.ca_url,
            "--fingerprint", fingerprint,
            "--force",
        ]

        self._run(cmd, "failed to obtain ssh certificate")

    def _get_ca_fingerprint(self) -> str:
        if self.ca_fingerprint_path.exists():
            return self.ca_fingerprint_path.read_text().strip()

        proc = subprocess.run(
            ["step", "ca", "fingerprint", "--ca-url", self.ca_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if proc.returncode != 0:
            raise CertificateError("unable to fetch CA fingerprint")

        fingerprint = proc.stdout.strip()
        self.ca_fingerprint_path.write_text(fingerprint)
        return fingerprint

    def _run(self, cmd, error):
        proc = subprocess.run(cmd)
        if proc.returncode != 0:
            raise CertificateError(error)
