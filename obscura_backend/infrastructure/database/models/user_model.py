from infrastructure.database.database import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    recovery_key = Column(String)