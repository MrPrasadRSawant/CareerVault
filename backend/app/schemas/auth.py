from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ORMModel
from app.schemas.user import UserRead


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=1024)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=1024)
    new_password: str = Field(min_length=1, max_length=1024)


class Token(ORMModel):
    access_token: str
    token_type: str = "bearer"


class TokenWithUser(Token):
    user: UserRead
