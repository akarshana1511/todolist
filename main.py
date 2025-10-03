from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="TODO API",
    description="A simple TODO API to add, view, complete, and delete tasks",
    version="1.1.0"
)

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks: List[Task] = []

# Root route
@app.get("/", summary="Welcome", description="Welcome message for the TODO API", tags=["General"])
def read_root():
    return {"message": "Welcome to the TODO API! Visit /docs to see Swagger UI."}

# View all tasks (now also includes total count)
@app.get("/tasks", summary="View Tasks", description="Retrieve the list of all tasks", tags=["Tasks"])
def get_tasks():
    return {
        "total_tasks": len(tasks),
        "tasks": tasks
    }

# Add a new task
@app.post("/tasks", summary="Add Task", description="Add a new task to the TODO list", tags=["Tasks"])
def add_task(task: Task):
    tasks.append(task)
    return {
        "message": "Task added",
        "task": task,
        "total_tasks": len(tasks)
    }

# Mark task as completed
@app.put("/tasks/{task_id}", summary="Mark Completed", description="Mark a task as completed by its ID", tags=["Tasks"])
def mark_completed(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return {
                "message": "Task marked as completed",
                "task": task,
                "total_tasks": len(tasks)
            }
    return {"error": "Task not found"}

# Delete a task
@app.delete("/tasks/{task_id}", summary="Delete Task", description="Delete a task by its ID", tags=["Tasks"])
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {
        "message": "Task deleted",
        "total_tasks": len(tasks)
    }
