from typing import List, Union, Optional
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class NoteBase(BaseModel):
    title: str
    description: Union[str, None] = None


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_id: int
    last_edit: Union[datetime, None] = None

    class Config:
        orm_mode = True


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Union[str, None] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    hashed_password: str
    notes: List[Note] = []

    class Config:
        orm_mode = True