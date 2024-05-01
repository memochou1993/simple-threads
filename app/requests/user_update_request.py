from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
