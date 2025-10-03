from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Settings

settings = Settings()
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
