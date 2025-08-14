from abc import ABC, abstractmethod

class RecoveryKeyGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        """Generates a recovery key."""
        pass