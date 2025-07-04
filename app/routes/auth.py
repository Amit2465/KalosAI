from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.security import OAuth2PasswordBearer
import logging

from app.config import settings
from app.models.users import User
from app.schemas.users import UserOut, UsernameUpdate
from app.db.session import get_db

router = APIRouter(prefix="/v1/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger(__name__)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        sub = idinfo["sub"]
        user = db.query(User).filter(User.id == sub).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

@router.post("/google", response_model=UserOut)
async def google_auth(body: dict = Body(...), db: Session = Depends(get_db)):
    token = body.get("token")
    if not token:
        logger.warning("Google auth attempt with missing token.")
        raise HTTPException(status_code=400, detail="Token is required")
    try:
        logger.info("Attempting Google token verification.")
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        sub = idinfo["sub"]
        email = idinfo["email"]
        name = idinfo.get("name")
        picture = idinfo.get("picture")
        username = email.split("@")[0]

        user = db.query(User).filter(User.id == sub).first()
        if not user:
            user = User(
                id=sub,
                email=email,
                name=name,
                username=username,
                profile_photo=picture
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {email}")
        else:
            logger.info(f"User already exists: {email}")
        return user
    except ValueError as e:
        logger.error(f"Google token verification failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")
    

@router.patch("/username", response_model=UserOut)
async def update_username(
    payload: UsernameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if username already exists
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    current_user.username = payload.username
    db.commit()
    db.refresh(current_user)
    return current_user
