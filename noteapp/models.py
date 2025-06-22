from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

note_tag_table = Table(
    'note_tag',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    tags = relationship("Tag", secondary=note_tag_table, back_populates="notes")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    notes = relationship("Note", secondary=note_tag_table, back_populates="tags")
