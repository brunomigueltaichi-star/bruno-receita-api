def create_tasks(
    payload: CreateTasksRequest,
    authorization: Optional[str] = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "").strip()

    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    tasks = payload.tasks
    return {"status": "ok", "count": len(tasks)}
