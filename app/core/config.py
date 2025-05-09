from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from app.core.database import DATABASE_URL

import os

BASE_DIR = Path(__file__).parent.parent

class DbSettings(BaseModel):
    url: str = DATABASE_URL
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt_privet.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt_public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 1


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()