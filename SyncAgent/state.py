from cert import CertificateManager
from fs.metadata import file_metadata


class AgentStateMachine:
    def __init__(self, cfg, api):
        self.cfg = cfg
        self.api = api
        self.run_id = None
        self.cert_mgr = CertificateManager(
            key_path=cfg.ssh_key_path,
            cert_path=cfg.ssh_cert_path,
        )

    def run(self):
        self._ensure_certificate()
        self._register_run()
        self._push()
        self._pull()
        self._finalize()

    def _ensure_certificate(self):
        self.cert_mgr.ensure_valid_certificate()

    def _register_run(self):
        resp = self.api.post("/api/runs/", {
            "agent_id": self.cfg.agent_id,
        })
        self.run_id = resp["id"]

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
            p = self.cfg.push_dir / item.path
            if p.exists():
                observations.append({
                    **file_metadata(p, self.cfg.checksum),
                    "direction": "PUSH",
                    "change": item.change,
                })

        self.api.post("/api/file-observations/bulk/", {
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
        self.api.post(f"/api/runs/{self.run_id}/finalize/", {})
