from domain.repositories.refresh_token_repository import RefreshTokenRepo
from infrastructure.database.models.refresh_token_model import RefreshToken
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

class RefreshTokenRepoImpl(RefreshTokenRepo):
    def __init__(self, session: Session):
        self.session = session
        self.expiration = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30")
    def create(self,token_id: str, username: str,hashed_token: str, user_agent: str, user_os: str, user_browser: str):
        """This function is responsible for creating a new refresh token when the user logs in."""
        db_model = RefreshToken(
            token_id = token_id,
            username = username,
            token_hash = hashed_token,
            expires_at = datetime.now(timezone.utc) + timedelta(days=int(self.expiration)),
            created_at = datetime.now(timezone.utc),
            revoked = False,
            revoked_at = None,
            user_agent = user_agent,
            user_os = user_os,
            user_browser = user_browser
        )
        self.session.add(db_model)
        self.session.commit()
    def read(self, token_id: str):
        """This function is responsible for retrieving the refresh token from the database."""
        return self.session.query(RefreshToken).filter(RefreshToken.token_id == token_id).first()
    def update(self,token_id: str, new_token_id: str, new_secret: str, user_agent: str, revoked: bool=False, revoked_at: datetime=None):
        """This function is responsible for updating the refresh token."""
        db_model = self.session.query(RefreshToken).filter(RefreshToken.token_id == token_id).first()
        db_model.token_id = new_token_id
        db_model.token_hash = new_secret
        db_model.user_agent = user_agent
        db_model.revoked = revoked
        db_model.revoked_at = revoked_at
        self.session.commit()
        self.session.refresh(db_model)