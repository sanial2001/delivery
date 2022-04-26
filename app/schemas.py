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


class Order(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }


class UpdateStatus(BaseModel):
    order_status: Optional[str] = "IN=TRANSIT"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "DELIVERED"
            }
        }
