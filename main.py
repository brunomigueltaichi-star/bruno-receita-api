from pydantic import BaseModel
from typing import List, Optional
from fastapi import Header

class CreateTasksRequest(BaseModel):
    tasks: List[TaskIn]

@app.post("/tasks")
def create_tasks(
    payload: CreateTasksRequest,
    authorization: Optional[str] = Header(default=None)
):
    tasks = payload.tasks
    # resto do código continua igual
    return {"status": "ok", "count": len(tasks)}
