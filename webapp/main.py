from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime

from planner import Planner

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

def get_planner():
    return Planner()

# -------------------- TASKS --------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request, planner: Planner = Depends(get_planner)):
    tasks = planner.db.get_tasks()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.get("/add", response_class=HTMLResponse)
def add_task_form(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

@app.post("/add")
def add_task(
    title: str = Form(...),
    duration: int = Form(...),
    priority: str = Form(...),
    deadline: str = Form(...)
):
    planner = Planner()
    planner.add_task(title, duration, priority, deadline)
    planner.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    planner = Planner()
    planner.delete_task(task_id)
    planner.close()
    return RedirectResponse(url="/", status_code=303)

#reflection 
@app.get("/reflections", response_class=HTMLResponse)
def reflections(request: Request, planner: Planner = Depends(get_planner)):
    reflections = planner.db.conn.execute("SELECT entry, date FROM reflections ORDER BY date DESC").fetchall()
    return templates.TemplateResponse("reflections.html", {"request": request, "reflections": reflections})

@app.post("/reflections")
def add_reflection(entry: str = Form(...)):
    planner = Planner()
    today = datetime.today().strftime("%Y-%m-%d")
    planner.db.conn.execute("INSERT INTO reflections (entry, date) VALUES (?, ?)", (entry, today))
    planner.db.conn.commit()
    planner.close()
    return RedirectResponse(url="/reflections", status_code=303)

#reschedule 
@app.post("/reschedule")
def reschedule_tasks():
    planner = Planner()
    planner.reschedule_tasks()
    planner.close()
    return RedirectResponse(url="/", status_code=303)
