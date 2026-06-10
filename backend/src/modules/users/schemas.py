from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.models.enums import UserRole


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: UserRole

    model_config = {
        "from_attributes": True
    }