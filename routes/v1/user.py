from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserData, UserResponse, UserUpdateData
from sqlmodel import Session
from db.session import get_db_session as get_db
from db.repository.user import (
    create_user,
    get_user_with_email,
    update_user_details,
    get_current_user,
)

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("/", response_model=UserResponse)
async def create_user_path(user_data: UserData, db_session: Session = Depends(get_db)):
    if get_user_with_email(user_data.email, db_session) is not None:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )
    user = create_user(user_data=user_data, session=db_session)
    return user


@user_router.patch("/", response_model=UserResponse)
async def modify_user_details(
    user_data: UserUpdateData,
    db_session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = update_user_details(user_data, current_user, db_session)
    return user
