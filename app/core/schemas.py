from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    id: Optional[int] = None
    password: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    authorization: str = "Bearer"
    
class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True