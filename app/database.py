from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

URL_DATABASE = "mysql+pymysql://root:123456@localhost:3306/teacher_db"

engine = create_engine(URL_DATABASE, pool_size=10, max_overflow=20, pool_timeout=30)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
