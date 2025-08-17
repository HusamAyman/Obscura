from domain.repositories.user_repository import UserRepository
from domain.interfaces.jwt_tokens_generator import *
from passlib.context import CryptContext
from application.exceptions.exceptions import UserNotFound,UnAuthorizedAccess



class LoginUseCase:
    def __init__(self, repo: UserRepository, access: AccessTokenGenerator, refresh: RefreshTokenGenerator):
        self.repo = repo
        self.access_token_generator = access
        self.refresh_token_generator = refresh
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def execute(self, username: str, password: str) -> dict:
        user = self.repo.read(username)
        if user is None:
            raise UserNotFound()
        if not self.pwd_context.verify(password, user.hashed_password):
            raise UnAuthorizedAccess()
        access_token = self.access_token_generator.encode(username)
        refresh_token = self.refresh_token_generator.encode()
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
