from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

import os

BASE_DIR = Path(__file__).parent.parent

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:qwerzxcv@localhost:3306/mydb")

class DbSettings(BaseModel):
    url: str = DATABASE_URL
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt_privet.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt_public.pem"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 1


class Settings(BaseSettings):
    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()