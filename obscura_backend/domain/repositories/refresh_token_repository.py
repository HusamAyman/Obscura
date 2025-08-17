from abc import abstractmethod
from domain.repositories.crud import CRUD

class RefreshTokenRepo(CRUD):
    @abstractmethod
    def create(self, *args, **kwargs):
        """Abstract function used to save the token information in the database"""
        pass