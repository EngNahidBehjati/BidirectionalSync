from engine.action_model import Action


class DiffEngine:
    def __init__(self, storage_port):
        self._storage = storage_port



    def compare(self):
        conflicts = []
        normal_actions = []

        superior = self._storage.list_superior()
        agent = self._storage.list_agent()

        only_superior = superior - agent
        only_agent = agent - superior
        common = superior & agent

        self._check_files_only_on_superior(only_superior, conflicts, normal_actions)
        self.check_files_only_on_agent(only_agent, conflicts, normal_actions)
        self._compare_common(common, conflicts, normal_actions)

        return conflicts, normal_actions

    @staticmethod
    def _check_files_only_on_superior(files, conflicts, normal_actions):
        for f in files:
            normal_actions.append(
                Action.download(f)
            )
        return

    @staticmethod
    def check_files_only_on_agent(files, conflicts, normal_actions):
        for f in files:
            conflicts.append(
                Conflict.local_creation(f)
            )
        return


    def _compare_common(self, file, conflicts, normal_actions):
        s_meta = self._storage.stat_superior(file)
        a_meta = self._storage.stat_agent(file)

        if s_meta.type != a_meta.type:
            conflicts.append(Conflict.type_mismatch(file))
            return

        if s_meta.checksum == a_meta.checksum:
            if s_meta.metadata != a_meta.metadata:
                conflicts.append(Conflict.metadata_drift(file))
            return

        # content different
        if s_meta.modified > a_meta.modified:
            normal_actions.append(Action.download(file))
        else:
            conflicts.append(Conflict.local_modification(file))

