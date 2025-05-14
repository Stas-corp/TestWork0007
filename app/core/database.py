from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

HOST = os.getenv("DB_HOST", "localhost")
DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+mysqlconnector://root:qwerzxcv@{HOST}:3306/mydb")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()