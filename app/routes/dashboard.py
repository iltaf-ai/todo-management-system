from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

dashboard_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@dashboard_router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )

@dashboard_router.get("/todo-page", response_class=HTMLResponse)
def todo_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html"
    )