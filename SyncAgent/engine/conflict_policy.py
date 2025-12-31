class ConflictPolicy:
    def __init__(self, mode="rename"):
        self.mode = mode

    def resolve(self, changes):
        if self.mode == "overwrite":
            ...
        if self.mode == "skip":
            ...
        if self.mode == "rename":
            ...
        return resolved_changes
