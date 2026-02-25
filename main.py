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

def extract_token(authorization: Optional[str], x_api_key: Optional[str]) -> Optional[str]:
    if authorization:
        return authorization.replace("Bearer ", "").strip()
    if x_api_key:
        return x_api_key.strip()
    return None

@app.post("/tasks")
def create_tasks(
    payload: CreateTasksRequest,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None)
):
    token = extract_token(authorization, x_api_key)
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"status": "ok", "count": len(payload.tasks)}

@app.get("/tasks")
def list_tasks(
    date: Optional[str] = None,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None)
):
    token = extract_token(authorization, x_api_key)
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"tasks": [], "date": date}
