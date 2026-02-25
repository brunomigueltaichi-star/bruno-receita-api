from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

API_TOKEN = "bruno_receita_api_token_93xA7kQ"

class TaskIn(BaseModel):
    date: str
    title: str
    priority: str

class CreateTasksRequest(BaseModel):
    tasks: List[TaskIn]

@app.post("/tasks")
def create_tasks(
    payload: CreateTasksRequest,
    authorization: Optional[str] = Header(None)
):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "status": "ok",
        "count": len(payload.tasks)
    }

@app.get("/tasks")
def list_tasks():
    return {
        "tasks": []
    }
