from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100))
    password = Column(String(255))


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    work = Column(String(500))
    completed = Column(Boolean, default=False)