from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class TodoCreate(BaseModel):
    work: str
    completed: bool = False