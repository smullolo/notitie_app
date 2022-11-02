from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from . import models, schemas, utils
from fastapi import HTTPException
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_notes(db: Session, current_user_id, skip: int = 0, limit: int = 100, start_time: datetime = datetime.min,
              end_time: datetime = datetime.max):
    return db.query(models.Note).filter(
        models.Note.owner_id == current_user_id,
        models.Note.last_edit.between(start_time, end_time)
    ).offset(skip).limit(limit).all()


def update_user_note(db: Session, note: schemas.NoteUpdate, user_id: int, note_id: int):
    db_note = db.query(models.Note).filter(models.Note.owner_id == user_id, models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    note_data = note.dict(exclude_unset=True)
    for key, value in note_data.items():
        setattr(db_note, key, value)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def create_user_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_user_note(db: Session, user_id: int, note_id: int):
    db_note = db.query(models.Note).filter(models.Note.owner_id == user_id, models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return HTTPException(status_code=204, detail="deleted succesfully")