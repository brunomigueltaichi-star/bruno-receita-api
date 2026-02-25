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

def verify_token(authorization: Optional[str]):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing token")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization[len("Bearer "):].strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/tasks")
def create_tasks(
    payload: CreateTasksRequest,
    authorization: Optional[str] = Header(None)
):
    verify_token(authorization)
    return {"status": "ok", "count": len(payload.tasks)}

@app.get("/tasks")
def list_tasks(
    authorization: Optional[str] = Header(None),
    date: Optional[str] = None
):
    verify_token(authorization)
    return {"tasks": [], "date": date}
