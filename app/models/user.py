from sqlalchemy import Column, Integer, String, DateTime,Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
from enum import Enum as PyEnum
class Role(str, PyEnum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"

class User(Base):
    __tablename__ = 'user'  # Use of lowercase for table name

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100) , unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tasks = relationship('Task', back_populates='user')
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
