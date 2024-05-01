from pydantic import BaseModel, EmailStr, Field


class UserStoreRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
