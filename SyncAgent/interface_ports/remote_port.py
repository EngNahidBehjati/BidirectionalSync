# ports/remote_port.py

from abc import ABC, abstractmethod

class RemotePort(ABC):

    @abstractmethod
    def report_event(self, event: dict):
        pass

    @abstractmethod
    def report_conflict(self, conflict: dict):
        pass

    @abstractmethod
    def report_failure(self, error: dict):
        pass
