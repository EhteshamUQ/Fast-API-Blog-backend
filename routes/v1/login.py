from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.login import Token
from sqlmodel import Session
from db.session import get_db_session
from db.repository.user import get_user_with_email
from utils.security import create_access_token, validate_password


login_router = APIRouter(prefix="/login", tags=["Authentication"])


@login_router.post("/", response_model=Token)
def get_access_token(
    login_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db_session),
):
    user = get_user_with_email(login_data.username, session)
    if user is not None and validate_password(login_data.password, user.password):
        token = create_access_token(
            data={"id": user.id, "name": user.name, "role": user.role},
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=403, detail="Incorrect username or password")
