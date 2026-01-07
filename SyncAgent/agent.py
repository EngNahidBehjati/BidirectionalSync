from adapter.api_client import ApiClient
from lock_manager import LockManager, LockError
from schema.agent_config import AgentConfig
from certificate_manager import CertificateManager



class Agent:
    def __init__(self, config:AgentConfig):
        self.config = config
        self.lock = LockManager(config.lock_path)
        self.certificate_manager = CertificateManager(
            key_path=config.ssh_key,
            cert_path=config.ssh_cert,
            ca_url=config.ca_url,
            principal=config.principal,
            ca_fingerprint_path=config.ca_fp,
            min_valid_seconds=config.min_valid_seconds,
        )

        self.api_client = ApiClient(self.config.api_url, self.config.api_token)
        self.run_id = None


    def run(self):
        self._ensure_certificate()
        try:
            with self.lock:
                self._execute_sync()
        except LockError:
            return

    def _execute_sync(self):
        self._register_run()
        self._push()
        self._pull()
        self._finalize()

    def _ensure_certificate(self):
        self.certificate_manager.ensure()

    def _register_run(self):
        self.run_id = self.api_client.get_run(self.config.agent_id, self.lock.lock_start_time)

    def _push(self):
        cmd = [
            "rsync",
            "-a",
            "--partial",
            "--partial-dir=.rsync-partial",
            "--delay-updates",
            "--numeric-ids",
            "--no-owner",
            "--no-group",
            "--out-format=%i %n",
            "-e", ssh_cmd,
            f"{local_dir}/",
            f"{ssh_user}@{ssh_host}:{remote_dir}/",
        ]

        result = self.rsync_adapter.run_rsync(cmd)
        items = self.rsync_adapter.parse_rsync_output(result.stdout)

        observations = []
        for item in items:
            p = self.config.push_dir / item.path
            if p.exists():
                observations.append({
                    **file_metadata(p, self.config.checksum),
                    "direction": "PUSH",
                    "change": item.change,
                })

        self.api_client.post("/api/file-observations/bulk/", {
            "run_id": self.run_id,
            "items": observations,
        })

    def _pull(self):
        cmd = [
            "rsync",
            "-a",
            "--partial",
            "--partial-dir=.rsync-partial",
            "--delay-updates",
            "--numeric-ids",
            "--no-owner",
            "--no-group",
            "--out-format=%i %n",
            "-e", ssh_cmd,
            f"{local_dir}/",
            f"{ssh_user}@{ssh_host}:{remote_dir}/",
        ]
        self.rsync_adapter.run_rsync(cmd)

    def _finalize(self):
        self.api_client.post(f"/api/runs/{self.run_id}/finalize/", {})
