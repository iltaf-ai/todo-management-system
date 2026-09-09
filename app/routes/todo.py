
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.model import Todo
from app.schema import TodoCreate


todo_router = APIRouter()



@todo_router.post("/todo")
def todo_create(
    user: TodoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    todo_work = Todo(
        user_id=current_user.id,
        work=user.work,
        completed=user.completed
    )

    db.add(todo_work)
    db.commit()
    db.refresh(todo_work)

    return {
        "message": "Task created successfully",
        "todo": todo_work
    }




@todo_router.get("/todo")
def see_todo(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todos = db.query(Todo).filter(
        Todo.user_id == current_user.id
    ).all()

    return todos




@todo_router.put("/todo/{todo_id}")
def update_todo(
    todo_id: int,
    user: TodoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update this todo"
        )

    todo.work = user.work
    todo.completed = user.completed

    db.commit()
    db.refresh(todo)

    return {
        "message": "Todo updated successfully",
        "todo": todo
    }




@todo_router.delete("/todo/{todo_id}")
def deleted_todo(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this todo"
        )

    db.delete(todo)
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }
