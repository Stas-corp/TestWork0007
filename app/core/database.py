from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST")
DATABASE=os.getenv("MYSQL_DATABASE")
PASSWORD=os.getenv("MYSQL_ROOT_PASSWORD")
DATABASE_URL = f"mysql+mysqlconnector://root:{PASSWORD}@{HOST}:3306/{DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()