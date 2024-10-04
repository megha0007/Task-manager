from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime
class StatusChoices(str, Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    
    
class PriorityChoices(str, Enum):
    high = 'High'
    medium = 'Medium'
   
# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    
    
class TaskCreate(BaseModel):
    title:str
    description:str
    status: Optional[StatusChoices] = 'todo'
    priority:Optional[PriorityChoices] = 'High'
    due_date:datetime
    user_id:int
    
class TaskUpdate(BaseModel):
    title:str
    description:str
    status: Optional[StatusChoices] = 'todo'
    priority:Optional[PriorityChoices] = 'High'
   