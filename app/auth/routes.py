import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core import models, schemas
from app.auth import utils as auth_utils
from app.dependencies import get_db

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not auth_utils.validate_password(password, user.hashed_password):
        return None
    return user


@router.post("/register", response_model=schemas.Token)
def register(
    user_data: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth_utils.hash_password(user_data.password)
    new_user = models.User(name=user_data.name, email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "access_token": auth_utils.create_access_token(user_data),
        "refresh_token": auth_utils.create_refresh_token(user_data),
    }


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user_data = schemas.UserCreate(
        name=user.name,
        email=user.email,
        password=""
    )
    return {
        "access_token": auth_utils.create_access_token(user_data),
        "refresh_token": auth_utils.create_refresh_token(user_data),
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    refresh_token: str, 
    db: Session = Depends(get_db)
):
    try:
        payload = auth_utils.decode_jwt(refresh_token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    user_data = schemas.UserCreate(
        name=user.name,
        email=user.email,
        password=""
    )
    return {
        "access_token": auth_utils.create_access_token(user_data),
        "refresh_token": auth_utils.create_refresh_token(user_data),
    }