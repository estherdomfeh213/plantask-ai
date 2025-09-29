from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os 

from planner import Planner

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

def get_planner():
    return Planner()

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
