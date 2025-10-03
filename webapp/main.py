from fastapi import FastAPI, Form, Depends
from fastapi.responses import RedirectResponse
from planner import Planner
from datetime import date

app = FastAPI()
planner = Planner()

def get_planner():
    return planner

@app.get("/")
def home():
    tasks = planner.list_tasks()
    reflections = planner.list_reflections()
    return {"tasks": tasks, "reflections": reflections}

@app.post("/add")
def add_task(title: str = Form(...), duration: int = Form(...),
             priority: str = Form(...), deadline: str = Form(...)):
    planner.add_task(title, duration, priority, deadline)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    planner.delete_task(task_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/reflections")
def reflections(planner: Planner = Depends(get_planner)):
    return {"reflections": planner.list_reflections()}

@app.post("/reflections")
def add_reflection(reflection: str = Form(...)):
    today = date.today().isoformat()
    planner.add_reflection(reflection, today)
    return RedirectResponse(url="/reflections", status_code=303)

@app.post("/reschedule")
def reschedule_tasks():
    planner.reschedule_tasks()
    return RedirectResponse(url="/", status_code=303)
