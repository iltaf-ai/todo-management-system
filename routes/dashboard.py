from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

dashboard_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@dashboard_router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )