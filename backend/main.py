from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

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

tasks = []
next_task_id = 1

@app.get("/tasks/{id}", response_model=TaskResponse)
def return_task(id: int):
    for task in tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(completed: Optional[bool] = None):
    if completed is not None:
        return [task for task in tasks if task.completed == completed]
    return tasks

@app.post("/tasks", status_code=201, response_model=TaskCreatedResponse)
def create_task(task: TaskCreate):
    global next_task_id
    new_task = TaskResponse(id=next_task_id, title=task.title, completed=task.completed)
    tasks.append(new_task)
    next_task_id += 1
    return {"message": "Task created successfully", "task": new_task}

@app.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, task: TaskCreate):
    for i, existing_task in enumerate(tasks):
        if existing_task.id == id:
            updated_task = TaskResponse(id=id, title=task.title, completed=task.completed)
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{id}", response_model=TaskResponse)
def patch_task(id: int, task: TaskUpdate):
    for i, existing_task in enumerate(tasks):
        if existing_task.id == id:
            updated_task = existing_task.model_copy(update=task.model_dump(exclude_unset=True))
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for i, task in enumerate(tasks):
        if task.id == id:
            del tasks[i]
            return
    raise HTTPException(status_code=404, detail="Task not found")
