from typing import Dict, Optional
from bcrypt import gensalt, hashpw, checkpw
from jose import jwt
from .config import Configuration
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException


def encrypt_password(password: str):
    return hashpw(password.encode(), gensalt(rounds=5))


def validate_password(plain_password: str, hashed_pw: bytes) -> bool:
    return checkpw(plain_password.encode(), hashed_password=hashed_pw)


# TODO: Serialize Enum Role
def create_access_token(data: Dict, expires_on: Optional[int] = None) -> str:
    to_encode = data.copy()
    print(to_encode)
    to_encode.update(
        {
            "exp": datetime.now()
            + timedelta(
                expires_on if expires_on is not None else Configuration.expiry_time
            )
        }
    )
    return jwt.encode(
        to_encode,
        key=Configuration.JWT_KEY,
        algorithm="HS256",
    )


def decode_token(token: str):
    try:
        return jwt.decode(token=token, key=Configuration.JWT_KEY, algorithms="HS256")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid Token")


oauth2_scheme = OAuth2PasswordBearer("v1/login")
