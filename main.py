from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class note(BaseModel):
    id:int
    name:str
    content:str

notes = [
    note(id=1,name="Rudra Bansal",content="name"),
    note(id=2,name="Jaypee Institute",content="college"),
    note(id=3,name="FastAPI",content="learning"),
    note(id=5,name="SQL",content="database")
]

@app.get("/notes")
def get_all_notes():
    return notes

@app.get("/notes/{id}")
def get_node(id:int):
    if(id<1):
        raise HTTPException(status_code=404,detail="Invalid Id")
    
    for i in range (len(notes)):
        if(id==notes[i].id):
            return notes[i]
    return "note not found"

@app.post("/notes")
def add_note(newnote:note):
    notes.append(newnote)
    return newnote

@app.put("/notes/{id}")
def update_note(id:int,updated_note:note):
    for i in range(len(notes)):
        if(id == notes[i].id):
            notes[i]=updated_note
            return "Product updated successfully!!"
    return "No product found"

@app.delete("/notes/{id}")
def delete_note(id:int):
    for i in range(len(notes)):
        if(id == notes[i].id):
            del notes[i]
            return "Note Deleted!!"
    return "No note found"