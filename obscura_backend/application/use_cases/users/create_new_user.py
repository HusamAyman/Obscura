from domain.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from application.schemas.create_account import CreateAccountSchema
from domain.entities.user_entity import UserEntity
from domain.interfaces.recovery_key_generator import RecoveryKeyGenerator
from application.exceptions.exceptions import UserAlreadyExists


class CreateAccountUseCase:
    def __init__(self, repo: UserRepository, key_generator: RecoveryKeyGenerator):
        self.repo = repo
        self.key_generator = key_generator

    def execute(self, user_data: CreateAccountSchema) -> str:
        user = self.repo.read(username=user_data.username)
        if user is not None:
            raise UserAlreadyExists(user_data.username)
        recovery_key = self.key_generator.generate()
        new_user = UserEntity(
            username = user_data.username,
            first_name= user_data.first_name,
            last_name= user_data.last_name,
            hashed_password=user_data.password,
            recovery_key=recovery_key,
        )
        new_user.create_hash_password(user_data.password)
        new_user.hash_recovery_key(recovery_key)
        self.repo.create(new_user)
        return recovery_key
