from domain.repositories.user_repository import UserRepository
from application.exceptions.exceptions import WrongPassword, DuplicatePassword

class ChangePassUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    def execute(self, username: str, old_password: str, new_password: str):
        user = self.repo.read(username)
        if not user.validate_password(old_password):
            raise WrongPassword()
        if user.validate_password(new_password):
            raise DuplicatePassword()
        user.create_hash_password(new_password)
        self.repo.update_password(username, user.hashed_password)