from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')

fast_api_sessionmaker = FastAPISessionMaker(DATABASE_URL)

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"}, pool_size=5, max_overflow=0)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine, expire_on_commit=True)

Base = declarative_base()
