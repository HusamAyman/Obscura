from domain.repositories.refresh_token_repository import RefreshTokenRepo
from domain.interfaces.jwt_tokens_generator import AccessTokenGenerator, RefreshTokenGenerator
from passlib.context import CryptContext
from application.exceptions.exceptions import UnAuthorizedAccess, TokenNotFound
from application.services.user_agent import UserAgentWrapper
from datetime import datetime, timezone

class RefreshUseCase:
    def __init__(self, repo: RefreshTokenRepo, access: AccessTokenGenerator, refresh: RefreshTokenGenerator):
        self.repo = repo
        self.access = access
        self.refresh = refresh
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def excute(self, token: str, username: str, user_agent: str) -> dict:
        token_id, secret = token.split(":")
        db_model = self.repo.read(token_id)
        #Check if the refresh token exist
        if db_model is None:
            raise TokenNotFound()
        # Check if the token matches with repository
        if not self.pwd_context.verify(secret, db_model.token_hash):
            raise UnAuthorizedAccess()
        # Check if the token belongs to the token owner, or is the token revoked or not
        if db_model.username != username or db_model.revoked == True:
            raise UnAuthorizedAccess()
        # Check if request came from the token owner device or not.
        ua = UserAgentWrapper(db_model.user_agent)
        ua_info = ua.parse_user_agent()
        user_os = ua_info["os"]
        user_browser = ua_info["browser"]
        if db_model.user_agent != user_agent:
            #if db_model.user_os != user_os or db_model.user_browser != user_browser:
                self.repo.update(
                    token_id=token_id,
                    new_token_id=token_id,
                    new_secret=secret,
                    user_agent=user_agent,
                    revoked=True,
                    revoked_at=datetime.now(timezone.utc)
                )
                raise UnAuthorizedAccess()
        # Generate new access/refresh tokens
        new_access_token = self.access.encode(username)
        new_refresh_token = self.refresh.encode()
        new_token_id, new_secret = new_refresh_token.split(":")
        self.repo.update(
            token_id=token_id,
            new_token_id=new_token_id,
            new_secret = self.pwd_context.hash(new_secret),
            user_agent = user_agent,
        )
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
