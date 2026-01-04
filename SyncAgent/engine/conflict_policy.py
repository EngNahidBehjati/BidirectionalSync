from engine.conflict_types import ConflictType
from engine.decision_model import Decision

class ConflictPolicy:
    def resolve(self, conflict):
        raise NotImplementedError

class DefaultConflictPolicy(ConflictPolicy):
    _MAPPING = {
        ConflictType.LOCAL_MODIFICATION: Decision.BACKUP_AND_PULL,
        ConflictType.LOCAL_DELETION: Decision.PULL_UPDATE,
        ConflictType.LOCAL_CREATION: Decision.REPORT_ONLY,
        ConflictType.TYPE_MISMATCH: Decision.FAIL_FAST,
        ConflictType.METADATA_DRIFT: Decision.PULL_UPDATE,
        ConflictType.UNSUPPORTED_STATE: Decision.FAIL_FAST,
    }

    def resolve(self, conflict):
        return self._MAPPING.get(
            conflict.type,
            Decision.FAIL_FAST  # fail safe
        )


class LenientPolicy(DefaultConflictPolicy):
    _MAPPING = {
        **DefaultConflictPolicy._MAPPING,
        ConflictType.LOCAL_CREATION: Decision.IGNORE,
    }
