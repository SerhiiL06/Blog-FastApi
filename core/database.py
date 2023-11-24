from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./blog.db/"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
