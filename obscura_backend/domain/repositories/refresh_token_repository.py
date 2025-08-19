from abc import abstractmethod
from domain.repositories.crud import CRUD

class RefreshTokenRepo(CRUD):
    @abstractmethod
    def create(self, *args, **kwargs):
        """Abstract function used to save the refresh token information in the database"""
        pass
    @abstractmethod
    def read(self, *args, **kwargs):
        """Abstract function used to read the refresh token information from the database"""
        pass
    @abstractmethod
    def update(self, *args, **kwargs):
        """Abstract function used to update refresh token"""