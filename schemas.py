from click import password_option
from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    gender: str


class UserUpdateRequest(UserCreateRequest):
    pass
