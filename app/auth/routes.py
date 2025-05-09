from dotenv import load_dotenv
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session

from app.core import models, schemas
from app.auth import utils as auth_utils
import app.dependencies as app_depend

load_dotenv()

http_bearer = HTTPBearer()
router = APIRouter(tags=["Auth"])

def authenticate_user(db: Session, email: str, password: str):
    user = app_depend.get_user_by_email(db, email)
    if not user or not auth_utils.validate_password(password, user.hashed_password):
        return None
    return user


@router.post("/register", response_model=schemas.Token)
def register(
    user_data: schemas.UserSchema, 
    db: Session = Depends(app_depend.get_db)
):
    if app_depend.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth_utils.hash_password(user_data.password)
    new_user = models.User(
        name=user_data.name, 
        email=user_data.email, 
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "access_token": auth_utils.create_access_token(user_data),
        "refresh_token": auth_utils.create_refresh_token(user_data)
    }


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(app_depend.get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user_data = schemas.UserSchema(
        name=user.name,
        email=user.email,
        password=""
    )
    return {
        "access_token": auth_utils.create_access_token(user_data),
        "refresh_token": auth_utils.create_refresh_token(user_data)
    }


@router.post("/aboutme")
def auth_user_self_info(
    user: models.User = Depends(app_depend.get_current_auth_user)
):
    return schemas.UserSchema.model_validate(user).model_dump(exclude={'password'})


@router.post("/refresh")
def refresh_token(
    refresh_token: str, 
    db: Session = Depends(app_depend.get_db)
):
    try:
        payload = auth_utils.decode_jwt(refresh_token)
        user_email = payload.get("sub")
        token_type = payload.get(auth_utils.TOKEN_TYPE_FIELD)
        user = app_depend.get_user_by_email(db, user_email)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token. {e}")
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if token_type != auth_utils.REFRESH_TOKEN_TYPE:
        raise HTTPException(status_code=401, detail="Token not refresh type")
    user_data = schemas.UserSchema(
        name=user.name,
        email=user.email,
    )
    return {
        "access_token": auth_utils.create_access_token(user_data)
    }