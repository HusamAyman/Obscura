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
    def create(self, username: str,hashed_token: str, user_agent: str, ip_addr: str):
        db_model = RefreshToken(
            username = username,
            token_hash = hashed_token,
            expires_at = datetime.now(timezone.utc) + timedelta(days=int(self.expiration)),
            created_at = datetime.now(timezone.utc),
            revoked = False,
            revoked_at = None,
            user_agent = user_agent,
            ip_address = ip_addr
        )
        self.session.add(db_model)
        self.session.commit()
