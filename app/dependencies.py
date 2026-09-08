
from app.model import User
from fastapi import HTTPException, Depends 
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.config import settings
from datetime import datetime, timedelta, timezone
from app.database import get_db
from sqlalchemy.orm import Session

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_EXPIRE_TOKEN_TIME = settings.ACCESS_EXPIRE_TOKEN_TIME


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# JWT authentication
auth_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Create JWT token
def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_EXPIRE_TOKEN_TIME
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Token is created",
        "token": token
    }


#token auth_sechmas

def get_username_from_token(
    token: str = Depends(auth_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("username")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

#current user
def get_current_user(username : str = Depends(get_current_user) , db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
         raise HTTPException(
            status_code=401,
            detail="username not found"
           )
    return username 