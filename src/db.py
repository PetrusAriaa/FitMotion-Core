from os import getenv
import os
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

if not os.getenv('SERVER_ENV') == 'production':
    load_dotenv(".env.development")

engine = create_engine(getenv("PG_URL"), pool_size=100, pool_recycle=15)

db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    yield db()