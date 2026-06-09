from pydantic import BaseModel
from pydantic import EmailStr


class RegisterRequest(BaseModel):
    company_name: str
    industry: str

    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    user_id: str
    role: str