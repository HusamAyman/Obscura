from dotenv import load_dotenv
from domain.interfaces.jwt_tokens_generator import *
from datetime import datetime, timedelta, timezone
import os
from jose import jwt, JWTError
import uuid
from fastapi import HTTPException
import secrets

load_dotenv()

class AccessTokenGeneratorImpl(AccessTokenGenerator):
    def __init__(self):
        self.__secret_key = os.getenv("SECRET_KEY")
        self.__algorithm = os.getenv("ALGORITHM")
        self.__access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    def encode(self, username: str):
        # iat stands for issued at, it indicates the time at which the token has been created
        iat = int(datetime.now(timezone.utc).timestamp())
        expiration = datetime.now(timezone.utc) + timedelta(minutes=self.__access_token_expire_minutes)
        payload = {
            "sub" : username,
            "iat" : iat,
            "exp" : expiration,
            "type": "access"
        }
        # TODO: check the token dtype, weather its a string or other thing
        return jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm)
    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
            payload = {
                "username": payload.get("sub"),
                "iat": payload.get("iat"),
                "exp": payload.get("exp"),
                "type": payload.get("type")
            }
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail=f"An error occurred due to {JWTError}")



class RefreshTokenGeneratorImpl(RefreshTokenGenerator):
    def __init__(self):
        self.__algorith = os.getenv("ALGORITHM")
        self.__secret_key = os.getenv("SECRET_KEY")
        self.__refresh_token_expire_minutes = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    def encode(self) -> str:
        return secrets.token_urlsafe(64)