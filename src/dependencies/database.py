from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base 
from .config import DATABASE_URI
Base = declarative_base()
 
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
       db.close()