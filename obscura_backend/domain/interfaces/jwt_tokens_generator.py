from abc import ABC, abstractmethod


class AccessTokenGenerator(ABC):
    @abstractmethod
    def encode(self, username: str) -> str:
        """Encodes a username into an access token."""
        pass

    @abstractmethod
    def decode(self, token: str) -> dict:
        """Decodes an access token into its payload."""
        pass



class RefreshTokenGenerator(ABC):
    @abstractmethod
    def encode(self) -> str:
        """Encodes a username into a refresh token."""
        pass