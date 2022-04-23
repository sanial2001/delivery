from pydantic import BaseModel
from typing import Optional


class Signup(BaseModel):
    id: Optional[str]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "sam",
                "email": "sam123@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }


class Login(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None
