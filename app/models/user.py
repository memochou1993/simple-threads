from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    user_id: Optional[str] = None
    name: str = Field(..., min_length=1)
    email: EmailStr
