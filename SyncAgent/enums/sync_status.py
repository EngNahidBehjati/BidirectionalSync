from enum import Enum


class SyncStatus(Enum):
    Success = "SUCCESS"
    Partial = "PARTIAL"
    Failed = "FAILED"