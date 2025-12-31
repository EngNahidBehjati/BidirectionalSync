class SyncEngine:
    def __init__(self, config, ftp, api, diff, conflict):
        self.cfg = config
        self.ftp = ftp
        self.api = api
        self.diff = diff
        self.conflict = conflict

    def run(self):
        self.api.heartbeat()  # اتصال به سرور
        remote_files = self.ftp.list_files()
        local_files = self.diff.list_local()

        changes = self.diff.compare(local_files, remote_files)
        actions = self.conflict.resolve(changes)

        for action in actions:
            if action.type == "PULL":
                self.ftp.download(action.remote, action.local)
            elif action.type == "PUSH":
                self.ftp.upload(action.local, action.remote)

        self.api.send_run_status({"changes": actions})
