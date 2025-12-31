from typing import List

from config.schema import AgentConfig
from engine.decision_model import SyncAction
from interface_ports.storage_port_interface import IStoragePort


class FileDiff:
    def __init__(self, storage: IStoragePort, config: AgentConfig):
        self.storage = storage
        self.cfg = config

    def compare(self):
        local = set(self.storage.list_local())
        remote = set(self.storage.list_remote())

        actions = []

        # 1️⃣ فقط در Remote → باید بگیریم (PULL)
        for f in remote - local:
            actions.append(SyncAction(type="PULL", file=f, reason="remote_new"))

        # 2️⃣ فقط در Local → باید بفرستیم (PUSH)
        for f in local - remote:
            actions.append(SyncAction(type="PUSH", file=f, reason="local_new"))

        # 3️⃣ فایل‌هایی که قبلاً بوده و الان در Remote حذف شده → DELETE_LOCAL
        # (این حالت زمانی معنی دارد که Log داریم یا قبلاً وجودش ثبت شده)
        # این را در مرحله Storage Logging اضافه خواهیم کرد

        # 4️⃣ فایل‌های مشترک → بررسی timestamp
        for f in local & remote:
            lt = self.storage.stat_local(f)
            rt = self.storage.stat_remote(f)

            if lt > rt:
                actions.append(SyncAction(type="UPDATE_REMOTE", file=f, local_ts=lt, remote_ts=rt))
            elif rt > lt:
                actions.append(SyncAction(type="UPDATE_LOCAL", file=f, local_ts=lt, remote_ts=rt))
            elif abs(lt - rt) > 0 and lt != rt:
                actions.append(SyncAction(
                    type="CONFLICT",
                    file=f,
                    local_ts=lt,
                    remote_ts=rt,
                    reason="both_modified"
                ))
            else:
                continue

        return actions
