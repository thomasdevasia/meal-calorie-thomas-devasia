from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	first_name = Column(String(100), nullable=False)
	last_name = Column(String(100), nullable=False)
	email = Column(String(255), unique=True, nullable=False)
	password_hash = Column(String(255), nullable=False)


class UserSearchHistory(Base):
	__tablename__ = 'user_search_history'

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
	search_keyword = Column(String(255), nullable=False)
	dish_name = Column(String(255), nullable=False)
	calories_per_serving = Column(Integer, nullable=False)
	total_calories = Column(Integer, nullable=False)
	protein_per_serving = Column(Integer, nullable=False)
	fat_per_serving = Column(Integer, nullable=False)
	carbohydrates_per_serving = Column(Integer, nullable=False)
	source = Column(String(255))
	searched_at = Column(DateTime, default=lambda: datetime.now(UTC))
