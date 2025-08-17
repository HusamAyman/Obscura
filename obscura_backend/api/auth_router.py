from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from application.use_cases.auth.login_use_case import LoginUseCase
from application.use_cases.auth.save_refresh_token import SaveTokenUseCase
from infrastructure.services.jwt_tokens_generator_impl import *
from infrastructure.repositories_impl.user_repo_impl import UserRepoImpl
from infrastructure.database.dependencies import db_dependency
from infrastructure.repositories_impl.refresh_token_repo_impl import RefreshTokenRepoImpl
from application.exceptions.exceptions import UserNotFound, UnAuthorizedAccess
from api.exceptions.excpetions import HTTPUserNotFound, HTTPUnauthorizedAccess

router = APIRouter(
    prefix="/auth",
    tags = ["Authentication & Authorization"]
)

@router.post("/tokens", status_code=201)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request, db: db_dependency):
    repo = UserRepoImpl(db)
    access_token_generator = AccessTokenGeneratorImpl()
    refresh_token_generator = RefreshTokenGeneratorImpl()
    use_case = LoginUseCase(
        repo,
        access_token_generator,
        refresh_token_generator
    )
    try:
        result = use_case.execute(form_data.username, form_data.password)
        token_repo = RefreshTokenRepoImpl(db)
        save_token_use_case = SaveTokenUseCase(token_repo)
        save_token_use_case.execute(
            form_data.username,
            result.get("refresh_token"),
            request.headers.get("User-Agent"),
            request.client.host
        )
        return {
            "access_token": result.get("access_token"),
            "refresh_token": result.get("refresh_token"),
            "token_type": "bearer"
        }
    except UserNotFound:
        raise HTTPUserNotFound(form_data.username)
    except UnAuthorizedAccess:
        raise HTTPUnauthorizedAccess()