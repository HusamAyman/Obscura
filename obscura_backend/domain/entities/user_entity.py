from passlib.context import CryptContext


class UserEntity:
    def __init__(self, username: str, first_name: str, last_name: str, hashed_password: str,user_id:int = None, recovery_key: str = None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.recovery_key = recovery_key
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def has_recovery_key(self) -> bool:
        if self.recovery_key is None:
            return False
        return True
    def create_hash_password(self, password: str) -> str:
        self.hashed_password = self.pwd_context.hash(password)
        return self.hashed_password
    def hash_recovery_key(self, recovery_key: str) -> str:
        self.recovery_key = self.pwd_context.hash(recovery_key)
        return self.recovery_key