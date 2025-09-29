from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from planner import Planner

app = FastAPI()
planner = Planner()


def get_planner():
    return planner


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    tasks = planner.list_tasks()
    return {"tasks": tasks}


@app.post("/add")
def add_task(title: str = Form(...), duration: int = Form(...),
             priority: str = Form(...), deadline: str = Form(...)):
    planner.add_task(title, duration, priority, deadline)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete")
def delete_task(task_id: int = Form(...)):
    planner.delete_task(task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/reflections")
def add_reflection(entry: str = Form(...)):
    planner.add_reflection(entry)
    return RedirectResponse(url="/", status_code=303)
