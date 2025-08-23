from infrastructure.repositories_impl.user_repo_impl import UserRepoImpl
from application.use_cases.users.create_new_user import CreateAccountUseCase
from application.use_cases.users.change_password import ChangePassUseCase
from application.use_cases.users.reset_password import ResetPassUseCase
from api.schemas.create_account import CreateAccountSchema
from api.dependencies.database_dep import db_dependency
from infrastructure.services.recovery_key_generator import SecureRecoveryKeyGenerator
from api.exceptions.excpetions import HTTPUserAlreadyExists, InternalServerError, HTTPDuplicatePassword, HTTPWrongPassword, HTTPInvalidRecoveryKey
from application.exceptions.exceptions import UserAlreadyExists, ApplicationBug, WrongPassword, DuplicatePassword, InvalidRecoveryKey
from fastapi import APIRouter
from api.dependencies.user_dep import user_dependency


router = APIRouter(
    prefix="/users",
    tags=["User Domain"]
)

@router.post("/create-new-account", status_code=201)
def create_new_account(user_name: str, first_name: str, last_name: str, password: str, db: db_dependency):
    try:
        user_data = CreateAccountSchema(
            username=user_name,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user_repo = UserRepoImpl(session=db)
        key_generator = SecureRecoveryKeyGenerator()
        create_account_use_case = CreateAccountUseCase(repo=user_repo, key_generator=key_generator)
        recovery_key = create_account_use_case.execute(user_data)
        return {"message": f"Your recovery key is {recovery_key}"}
    except UserAlreadyExists:
        raise HTTPUserAlreadyExists(user_name)
    except ApplicationBug as e:
        raise InternalServerError(detail=e.message)


@router.put("/change-password", status_code=201)
def change_user_password(old_password: str, new_password: str, user: user_dependency, db: db_dependency):
    repo = UserRepoImpl(session=db)
    use_case = ChangePassUseCase(repo=repo)
    try:
        use_case.execute(username=user["sub"],
                        old_password=old_password,
                        new_password=new_password
                        )
        return {"message": "Password has been changed successfully."}
    except WrongPassword:
        raise HTTPWrongPassword()
    except DuplicatePassword:
        raise HTTPDuplicatePassword()


@router.put("/reset-password", status_code=201)
def reset_user_password(username: str, recovery_key: str, new_password: str, db: db_dependency):
    repo = UserRepoImpl(db)
    use_case = ResetPassUseCase(repo=repo)
    try:
        use_case.execute(username, recovery_key, new_password)
        return {"message": "Your password has been reset successfully."}
    except InvalidRecoveryKey:
        raise HTTPInvalidRecoveryKey()
    except DuplicatePassword:
        raise HTTPDuplicatePassword()