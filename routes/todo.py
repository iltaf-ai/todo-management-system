from fastapi import HTTPException , Depends
from app.model import Todo
from app.schema import TodoCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import create_token , verify_password , get_current_user


todo_router = APIRouter()

@todo_router.post("/todo")
def todo_create(
    user : TodoCreate,
    db: Session = Depends(get_db),
   current_user= Depends(get_current_user) ,
    ):

    todo_work = Todo(
        user_id = current_user.id,
        work = user.work,
        completed = user.completed
    )


    db.add(todo_work)
    db.commit()

    return {
        "message" : "create Task Successfull"
    }


#Read Todo
@todo_router.get("/todo")
def see_todo(current_user = Depends(get_current_user) , db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(
        Todo.user_id == current_user.id
        ).all()
    return todo


#Update Todo
@todo_router.put("/todo/{todo_id}")

def update_todo(
    todo_id : int,
    user : TodoCreate,
    db:Session = Depends(get_db) ,
    current_user = Depends(get_current_user),
    
    ):


    todo = db.query(Todo).filter(
        Todo.id == todo_id
    ).first()

    if not todo :
        raise HTTPException (
            status_code=401,
            detail="Todo not found"
        )
    if todo.user_id != current_user.id:
        raise HTTPException (
        status_code=401,
        detail= "you can not update this todo"
       )

    todo.work = user.work
    todo.completed = user.completed

    db.commit()

    return {
      "message" : "You are todo is updated",
      "todo" : todo
    }


@todo_router.delete("/todo/{todo_id}")
def deleted_todo(
    todo_id : int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)
    ):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
            raise HTTPException(
                status_code=401,
                detail="Todo not found"
            )
        
    if todo.user_id !=  current_user.id:
            raise HTTPException (
                status_code=401,
                detail= "You are not able todo"
            )
    db.delete(todo)
    db.commit()
    return {
        "message" : "Todo work delete",
        "todo" : todo
    }
