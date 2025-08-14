from infrastructure.repositories_impl.user_repo_impl import UserRepoImpl
from application.use_cases.users.create_new_user import CreateAccountUseCase
from api.schemas.create_account import CreateAccountSchema
from infrastructure.database.dependencies import db_dependency
from infrastructure.services.recovery_key_generator import SecureRecoveryKeyGenerator
from api.exceptions.excpetions import HTTPUserAlreadyExists, InternalServerError
from application.exceptions.exceptions import UserAlreadyExists, ApplicationBug
from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["User Domain"]
)

@router.post("/create-new-account")
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