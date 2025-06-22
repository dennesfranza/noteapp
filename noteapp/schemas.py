from typing import List, Optional
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    class Config:
        orm_mode = True

class NoteBase(BaseModel):
    title: str
    description: Optional[str] = ""

class NoteCreate(NoteBase):
    tags: List[str] = []

class NoteUpdate(NoteBase):
    tags: List[str] = []

class Note(NoteBase):
    id: int
    tags: List[Tag] = []
    class Config:
        orm_mode = True
