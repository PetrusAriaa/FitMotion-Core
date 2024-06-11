from os import error, getenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

if not os.getenv('SERVER_ENV') == 'production':
    load_dotenv(".env.development")

engine = create_engine(getenv("PG_URL"))

db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    yield db()