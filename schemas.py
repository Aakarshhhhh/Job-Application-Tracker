from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ApplicationCreate(BaseModel):
    company_name : str
    status : str
    position : str
    application_link : Optional[str] = None
    notes : Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    position: str
    status: str
    application_link: Optional[str]
    notes: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        from_attributes = True
        
    