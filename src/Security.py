from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from model import Token, TokenData

class Hash:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    password_hash = PasswordHash.recommended()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    #Functions used
    def get_password_hash(self, password):
        return self.password_hash.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    @staticmethod
    async def get_current_user(token: Token, nombre: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token_string = token.access_token
            payload = jwt.decode(token_string, Hash.SECRET_KEY, algorithms=[Hash.ALGORITHM])
            username = payload.get("sub")
            
            if username == nombre:
                return True
            else:
                raise credentials_exception
                
        except Exception:
            raise credentials_exception