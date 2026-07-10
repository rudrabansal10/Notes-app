from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class note(BaseModel):
    id:int|None = None
    name:str
    content:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/notes")
def get_all_notes(db:db_dependency):
    result = db.query(models.Note).order_by(models.Note.id).all()
    return result

@app.get("/notes/{id}")
def get_node(id:int, db:db_dependency):
    result = db.query(models.Note).filter(models.Note.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return result

@app.post("/notes")
def add_note(newnote:note, db : db_dependency):
    if(db.query(models.Note).filter(models.Note.id == newnote.id).first()):
        raise HTTPException(status_code=409, detail="Note already exists")
    
    db_note = models.Note(
    id=newnote.id,
    name=newnote.name,
    content=newnote.content
    )
    db.add(db_note)
    db.commit()
    return "Note added !!"

@app.put("/notes/{id}")
def update_note(id:int,updated_note:note, db:db_dependency):
    result= db.query(models.Note).filter(models.Note.id == id).update({
        models.Note.name : updated_note.name,
        models.Note.content : updated_note.content
        })
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.commit()
    return "Note edited !!"

@app.delete("/notes/{id}")
def delete_note(id:int, db:db_dependency):
    result = db.query(models.Note).filter(models.Note.id == id).delete()

    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.commit()
    return "Note deleted !!"