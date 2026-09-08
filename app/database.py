from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session 
from app.config import settings


DATABASE_URI = settings.SQL_URL

engine = create_engine(
    DATABASE_URI,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()