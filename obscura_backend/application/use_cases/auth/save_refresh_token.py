from domain.repositories.refresh_token_repository import RefreshTokenRepo
from passlib.context import CryptContext
from application.services.user_agent import UserAgentWrapper


class SaveTokenUseCase:
    def __init__(self, repo: RefreshTokenRepo):
        self.repo = repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def execute(self, username: str, token: str, user_agent: str):
        ua_wrapper = UserAgentWrapper(user_agent)
        ua = ua_wrapper.parse_user_agent()
        user_os = ua.get("os")
        user_browser = ua.get("browser")
        token_id, secret = token.split(":")
        self.repo.create(
            token_id,
            username,
            self.pwd_context.hash(secret),
            user_agent,
            user_os,
            user_browser
        )