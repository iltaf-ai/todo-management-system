from sqlalchemy.orm import Session

from fastapi import HTTPException, Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.dependencies import verify_password, hash_password, create_token
from app.schema import UserCreate, UserLogin
from app.model import User


auth_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# =========================
# REGISTER API
# =========================

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


# =========================
# LOGIN API
# =========================

@auth_router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    user_existing = db.query(User).filter(
        User.username == user.username
    ).first()

    if not user_existing:
        return {
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


# =========================
# REGISTER PAGE
# =========================

@auth_router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


# =========================
# LOGIN PAGE
# =========================

@auth_router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )