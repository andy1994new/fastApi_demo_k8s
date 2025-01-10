from pydantic import BaseModel
from typing import List


class UserCreateSchema(BaseModel):
    name: str
    orders: List[int] = []


class UserSchema(BaseModel):
    id: int
    name: str
    orders: List[int]

    class Config:
        orm_mode = True
