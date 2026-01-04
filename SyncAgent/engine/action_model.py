from enum import Enum


class Action:
    def __init__(self, type_: ActionModelEnum, file=None):
        self.type = type_
        self.file = file

    @staticmethod
    def download(file):
        return Action(ActionModelEnum.DOWNLOAD_FILE, file=file)

    @staticmethod
    def delete(file):
        return Action(ActionModelEnum.DELETE_LOCAL_FILE, file=file)

    @staticmethod
    def backup(file):
        return Action(ActionModelEnum.BACKUP_LOCAL_FILE, file=file)

    @staticmethod
    def quarantine(file):
        return Action(ActionModelEnum.MOVE_TO_QUARANTINE, file=file)

    @staticmethod
    def report(file):
        return Action(ActionModelEnum.REPORT_EVENT, file=file)

    @staticmethod
    def fail(_):
        return Action(ActionModelEnum.FAIL_EXECUTION)


class ActionModelEnum(Enum):
    DOWNLOAD_FILE = "DOWNLOAD_FILE"
    DELETE_LOCAL_FILE = "DELETE_LOCAL_FILE"
    BACKUP_LOCAL_FILE = "BACKUP_LOCAL_FILE"
    MOVE_TO_QUARANTINE = "MOVE_TO_QUARANTINE"
    REPORT_EVENT = "REPORT_EVENT"
    FAIL_EXECUTION = "FAIL_EXECUTION"