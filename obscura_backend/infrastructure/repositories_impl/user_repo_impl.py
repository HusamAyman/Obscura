from domain.repositories.user_repository import UserRepository
from domain.entities.user_entity import UserEntity
from sqlalchemy.orm import Session
from infrastructure.database.models.user_model import User
from sqlalchemy.exc import IntegrityError

class UserRepoImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_data: UserEntity) -> None:
        try:
            db_model = User(
                username = user_data.username,
                first_name = user_data.first_name,
                last_name = user_data.last_name,
                hashed_password = user_data.hashed_password,
                recovery_key = user_data.recovery_key
            )
            self.session.add(db_model)
            self.session.commit()
        except IntegrityError as e:
            if "UNIQUE constraint failed" in str(e.orig):
                self.session.rollback()
                raise IntegrityError(e.statement, e.params, e.orig)
            else:
                self.session.rollback()
                raise Exception()
    
    def update(self, user_id: int, first_name: str, last_name: str) -> None:
        user = self.session.query(User).filter(User.user_id == user_id).first()
        # TODO: edit this code and add exception for user not found
        if user:
            user.first_name = first_name
            user.last_name = last_name
            self.session.commit()

    def delete(self, user_id: int, recovery_key: str) -> None:
        user = self.session.query(User).filter(User.user_id == user_id, User.recovery_key == recovery_key).first()  
        # TODO: edit this code and add exception for user not found
        if user:
            self.session.delete(user)
            self.session.commit()

    def read(self, username: str) -> UserEntity:
        user = self.session.query(User).filter(User.username == username).first()
        # TODO: edit this code and add exception for user not found
        if user is  None:
            return None
        user_info = UserEntity(
            user_id=user.user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            recovery_key=user.recovery_key
        )
        return user_info
        
    def update_password(self, user_id: int, new_password: str) -> None:
        user = self.session.query(User).filter(User.user_id == user_id).first() 
        # TODO: edit this code and add exception for user not found
        if user:
            user.hashed_password = new_password
            self.session.commit()