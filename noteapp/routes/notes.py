from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Note])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@router.post("/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    tag_objects = []
    for tag_name in note.tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tag_objects.append(tag)

    db_note = models.Note(title=note.title, description=note.description, tags=tag_objects)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.put("/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, updated_note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(models.Note).get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.description = updated_note.description

    tag_objects = []
    for tag_name in updated_note.tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tag_objects.append(tag)

    note.tags = tag_objects
    db.commit()
    db.refresh(note)
    return note
