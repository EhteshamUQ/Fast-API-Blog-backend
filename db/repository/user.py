from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from schemas.user import UserData, UserUpdateData
from utils.security import decode_token, oauth2_scheme

from ..models.User import User
from ..session import get_db_session


def create_user(user_data: UserData, session: Session) -> User:
    try:

        user = User(
            name=user_data.name,
            date_of_birth=user_data.date_of_birth,
            email=user_data.email,
            role=user_data.role,
            password=user_data.password,
        )
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error while creating user")


def get_user_with_email(email: str, session: Session) -> Optional[User]:
    try:
        statement = select(User).where(User.email == email)
        users = session.exec(statement).fetchmany(1)
        return None if len(users) == 0 else users[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error while fetching user")


def get_user_with_id(id: str, session: Session) -> Optional[User]:
    try:
        statement = select(User).where(User.id == id)
        users = session.exec(statement).fetchmany(1)
        return None if len(users) == 0 else users[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error while fetching user")


def update_user_details(
    user_data: UserUpdateData, user: User, session: Session
) -> User:
    try:
        user.name = user_data.name
        user.date_of_birth = user_data.date_of_birth
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error while updating user details")


def get_current_user(
    db_session: Session = Depends(get_db_session), token: str = Depends(oauth2_scheme)
):
    data = decode_token(token)
    print(data)
    return get_user_with_id(data.get("id"), db_session)
