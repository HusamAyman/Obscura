from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError
from infrastructure.services.jwt_tokens_generator_impl import AccessTokenGeneratorImpl
from api.exceptions.excpetions import HTTPUserNotFound, HTTPUnauthorizedAccess
from fastapi import Depends

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/tokens")

async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        # Decode the token to get the user information
        payload = AccessTokenGeneratorImpl().decode(token)
        if payload.get("sub") is None:
            raise HTTPUserNotFound("")
        return payload
    except JWTError:
        raise HTTPUnauthorizedAccess()
    except Exception as e:
        raise Exception(f"An error occurred while retrieving the current user: {str(e)}")


user_dependency = Annotated[dict, Depends(get_current_user)]