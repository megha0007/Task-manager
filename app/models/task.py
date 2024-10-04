from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
from enum import Enum as PyEnum
from models.user import User

class TaskStatus(str, PyEnum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(String(100), nullable=True)  # You might want to use an Enum here as well
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # Relationship to access the related User object from the Task object
    user = relationship('User', back_populates='tasks')

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
