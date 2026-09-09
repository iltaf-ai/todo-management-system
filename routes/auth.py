from sqlalchemy.orm import Session
from fastapi import HTTPException , Depends
from app.database import get_db
from fastapi import APIRouter
from app.dependencies import get_current_user , verify_password , hash_password , create_token
from app.schema import UserCreate  ,UserLogin
from app.model import User

auth_router = APIRouter()

#Register system
@auth_router.post("/register")

def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        return {
            "message": "User already exists"
        }

    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }


#Login system

@auth_router.post("/login")
def login(
    user:UserLogin ,
    db:Session = Depends(get_db)
):

    user_existing = db.query(User).filter(User.username == user.username).first()
    if not user_existing:
        return {#
        
            "message": "User not found"
        }
    
    password_verify = verify_password(
    user.password,
    user_existing.password
)

    if not password_verify:
        return {
            "message": "Incorrect password"
        }

    token_create = create_token({
        "username": user_existing.username
    })

    return {
    "message": "Login Successful",
    "token": token_create["token"]
    }
    
