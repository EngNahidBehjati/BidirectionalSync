from engine.decision_model import Decision
from engine.action_model import Action

class ExecutionMapper:
    _MAP = {
        Decision.IGNORE: [
            Action.report,
        ],
        Decision.REPORT_ONLY: [
            Action.report,
        ],
        Decision.PULL_UPDATE: [
            Action.download,
            Action.report,
        ],
        Decision.BACKUP_AND_PULL: [
            Action.backup,
            Action.download,
            Action.report,
        ],
        Decision.QUARANTINE_LOCAL: [
            Action.quarantine,
            Action.report,
        ],
        Decision.FAIL_FAST: [
            Action.report,
            Action.fail,
        ],
    }

    def map(self, decision, file):
        actions = []
        for factory in self._MAP.get(decision, []):
            actions.append(factory(file))
        return actions
