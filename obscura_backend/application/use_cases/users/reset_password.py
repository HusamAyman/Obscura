from domain.repositories.user_repository import UserRepository
from application.exceptions.exceptions import InvalidRecoveryKey, DuplicatePassword

class ResetPassUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    def execute(self,username: str, recovery_key: str, new_password: str):
        user = self.repo.read(username)
        if not user.validate_recovery_key(recovery_key):
            raise InvalidRecoveryKey()
        if user.validate_password(new_password):
            raise DuplicatePassword()
        user.create_hash_password(new_password)
        self.repo.update_password(username, user.hashed_password)