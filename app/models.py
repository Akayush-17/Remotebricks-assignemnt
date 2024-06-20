

from pydantic import BaseModel, Field, EmailStr
from typing import Optional,    List

class User(BaseModel):
    username:str = Field(...)
    email:EmailStr =Field(...)
    password: str= Field(...)

class UserInDB(BaseModel):  
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    linked_ids: List[str] = []


