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

@router.get("/", response_model=List[schemas.Tag])
def get_all_tags(db: Session = Depends(get_db)):
    return db.query(models.Tag).all()

@router.get("/{tag_id}", response_model=schemas.Tag)
def get_tag_with_notes(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).get(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
