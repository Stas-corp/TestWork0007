from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core import database, models
from app.auth import utils as auth_utils

http_bearer = HTTPBearer()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> models.User:
    token = credentials.credentials
    payload = auth_utils.decode_jwt(token)
    return payload

def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db)
) -> models.User:
    user_email = payload.get('sub')
    return get_user_by_email(db, user_email)