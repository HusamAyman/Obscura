from domain.repositories.refresh_token_repository import RefreshTokenRepo
from passlib.context import CryptContext


class SaveTokenUseCase:
    def __init__(self, repo: RefreshTokenRepo):
        self.repo = repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def execute(self, username: str, token: str, user_agent: str, ip_addr: str):
        self.repo.create(
            username,
            self.pwd_context.hash(token),
            user_agent,
            ip_addr
        )