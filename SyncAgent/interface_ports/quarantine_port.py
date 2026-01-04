# ports/quarantine_port.py

from abc import ABC, abstractmethod

class QuarantinePort(ABC):

    @abstractmethod
    def move(self, file: str):
        pass

    @abstractmethod
    def list(self) -> list[str]:
        pass
