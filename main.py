from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Tracker")

tasks = []
next_id = 1


class TaskIn(BaseModel):
    title: str
    done: bool = False


@app.post("/tasks")
def add_task(task: TaskIn):
    global next_id
    item = {"id": next_id, "title": task.title, "done": task.done}
    tasks.append(item)
    next_id += 1
    return item


@app.get("/tasks")
def list_tasks():
    return tasks


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskIn):
    for item in tasks:
        if item["id"] == task_id:
            item["title"] = task.title
            item["done"] = task.done
            return item
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for item in tasks:
        if item["id"] == task_id:
            tasks.remove(item)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
