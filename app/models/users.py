from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True) 
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    profile_photo = Column(String, unique=True, nullable=True)
    user_created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_subscribe = Column(Boolean, default=False)