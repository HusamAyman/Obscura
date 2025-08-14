from abc import abstractmethod
from domain.entities.user_entity import UserEntity
from domain.repositories.crud import CRUD


class UserRepository(CRUD):
    @abstractmethod
    def create(self, user_data: UserEntity) -> None:
        """Create a new user with the provided user_data."""
        pass
    @abstractmethod
    def update(self, user_id: int, first_name: str, last_name: str) -> None:
        """Update an existing user with the provided user_data."""
        pass
    @abstractmethod
    def delete(self, user_id: int, recovery_key: str) -> None:
        """Delete a user with the provided user_data."""
        pass
    @abstractmethod
    def read(self, username: str) -> UserEntity:
        """Read a user with the provided user_data."""
        pass
    @abstractmethod
    def update_password(self, user_id: int, new_password: str) -> None:
        """Update the password for an existing user."""
        pass