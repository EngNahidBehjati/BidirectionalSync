# ports/storage_port.py

from abc import ABC, abstractmethod

class StoragePort(ABC):

    # ---------- Superior (Authoritative / Read-Only) ----------

    @abstractmethod
    def list_superior(self) -> set[str]:
        pass

    @abstractmethod
    def stat_superior(self, file: str):
        pass

    @abstractmethod
    def read_superior(self, file: str):
        pass


    # ---------- Agent (Local / Restricted Write) ----------

    @abstractmethod
    def list_agent(self) -> set[str]:
        pass

    @abstractmethod
    def stat_agent(self, file: str):
        pass

    @abstractmethod
    def write_agent(self, file: str, content):
        pass

    @abstractmethod
    def delete_agent(self, file: str):
        pass

    @abstractmethod
    def backup_agent(self, file: str):
        pass
