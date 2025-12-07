from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class UserBackgroundCreate(BaseModel):
    role: Optional[str] = None
    programming_level: Optional[str] = None
    hardware_specs: Optional[str] = None
    software_experience: Optional[str] = None
    interest_field: Optional[str] = None
    preferred_language: Optional[str] = None
    goals: Optional[str] = None

class UserBackgroundRead(UserBackgroundCreate):
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Pydantic v2
