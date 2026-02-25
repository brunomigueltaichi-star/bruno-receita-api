import os
import json
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Bruno Receita API", version="1.0.0")

DATA_FILE = "data.json"
API_TOKEN = os.environ.get("API_TOKEN", "").strip()

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"tasks": []}

def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _require_auth(authorization: Optional[str]):
    if not API_TOKEN:
        raise HTTPException(status_code=500, detail="API_TOKEN não configurado.")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization em falta.")
    token = authorization.split(" ", 1)[1].strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido.")

class TaskIn(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD")
    title: str
    priority: str = Field(..., description="alta | media | baixa")

class TaskOut(TaskIn):
    id: str
    created_at: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks")
def create_tasks(tasks: List[TaskIn], authorization: Optional[str] = Header(default=None)):
    _require_auth(authorization)

    data = _load_data()
    now = datetime.now(timezone.utc).isoformat()

    created = 0
    for t in tasks:
        task_id = f"t_{len(data['tasks']) + 1}_{int(datetime.now().timestamp())}"
        data["tasks"].append({
            "id": task_id,
            "date": t.date,
            "title": t.title,
            "priority": t.priority,
            "created_at": now
        })
        created += 1

    _save_data(data)
    return {"status": "ok", "created": created}

@app.get("/tasks")
def list_tasks(
    date: Optional[str] = Query(default=None),
    authorization: Optional[str] = Header(default=None)
):
    _require_auth(authorization)

    data = _load_data()
    tasks = data.get("tasks", [])
    if date:
        tasks = [t for t in tasks if t.get("date") == date]
    return tasks
