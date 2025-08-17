from infrastructure.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    token_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
    user_agent = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)