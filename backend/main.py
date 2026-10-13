from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Task
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskCreate(BaseModel):
    title: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

class TaskCreatedResponse(BaseModel):
    message: str
    task: TaskResponse

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

@app.get("/tasks/{id}", response_model=TaskResponse)
def return_task(id: int, db: Session = Depends(get_db)):
    query = db.query(Task).filter(Task.id == id).first()
    if query:
        return query
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    return query.all()

@app.post("/tasks", status_code=201, response_model=TaskCreatedResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully", "task": new_task}

@app.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, task: TaskCreate, db: Session = Depends(get_db)):
    query = db.query(Task).filter(Task.id == id).first()
    if query:
        query.title = task.title
        query.completed = task.completed
        db.commit()
        db.refresh(query)
        return query
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{id}", response_model=TaskResponse)
def patch_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    query = db.query(Task).filter(Task.id == id).first()
    if query:
        if task.title is not None:
            query.title = task.title
        if task.completed is not None:
            query.completed = task.completed
        db.commit()
        db.refresh(query)
        return query
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    query = db.query(Task).filter(Task.id == id).first()
    if query:
        db.delete(query)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Task not found")
