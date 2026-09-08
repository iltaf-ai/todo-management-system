from fastapi import FastAPI


app  = FastAPI

from app.routes.auth import auth_router
from app.routes.todo import todo_router
from app.routes.dashboard import dashboard_router

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(dashboard_router)
