from engine.action_model import Action, ActionModelEnum


class SyncEngine:
    def __init__(
        self,
        diff_engine,
        conflict_policy,
        execution_mapper,
        storage_port,
        remote_port,
        quarantine_port=None,
    ):
        self._diff_engine = diff_engine
        self._conflict_policy = conflict_policy
        self._execution_mapper = execution_mapper
        self._storage = storage_port
        self._remote = remote_port
        self._quarantine = quarantine_port

    def run(self):
        try:
            conflicts, normal_actions = self._diff_phase()
            decisions = self._policy_phase(conflicts)
            action_plan = self._execution_mapping_phase(decisions, normal_actions)
            self._execution_phase(action_plan)
            self._report_success()

        except Exception as exc:
            self._handle_failure(exc)
            raise

    def _diff_phase(self):
        return self._diff_engine.compare()

    def _policy_phase(self, conflicts):
        decisions = []
        for conflict in conflicts:
            decision = self._conflict_policy.resolve(conflict)
            decisions.append(decision)
        return decisions

    def _execution_mapping_phase(self, decisions, normal_actions):
        action_plan = []

        for decision in decisions:
            actions = self._execution_mapper.map(decision)
            action_plan.extend(actions)

        action_plan.extend(normal_actions)
        return action_plan

    def _execution_phase(self, action_plan):
        for action in action_plan:
            self._execute_action(action)


    def _execute_action(self, action):
        if action.type == ActionModelEnum.DOWNLOAD_FILE:
            self._storage.download_from_superior(action.file)

        elif action.type == ActionModelEnum.DELETE_LOCAL_FILE:
            self._storage.delete_agent_file(action.file)

        elif action.type == ActionModelEnum.BACKUP_LOCAL_FILE:
            self._storage.backup_agent_file(action.file)

        elif action.type == ActionModelEnum.MOVE_TO_QUARANTINE:
            self._quarantine.move(action.file)

        elif action.type == ActionModelEnum.REPORT_EVENT:
            self._remote.report(action.file)

        elif action.type == ActionModelEnum.FAIL_EXECUTION:
            raise RuntimeError("Fail fast triggered")


    #todo Message Maker
    def _report_success(self):
        return self._remote.report({"status": "success"})

    def _handle_failure(self, exc):
        self._remote.report({
            "status": "failed",
            "reason": str(exc),
        })

