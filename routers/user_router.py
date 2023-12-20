from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from db.session import get_db
from typing import List
from routers.login_router import get_current_user_from_token
from db.models import User
from schemas.user_schema import CreateUserSchema, ShowUserSchema
import secrets
from repository import user

router = APIRouter()


@router.get("/all", response_model=List[ShowUserSchema])
def get_all_users(db:Session = Depends(get_db), current_user:User = Depends(get_current_user_from_token)):
    users = db.query(User).all()
    return users


@router.post("/create/",status_code = status.HTTP_201_CREATED)
def create_users(request: CreateUserSchema, db: Session = Depends(get_db)):
    db_phone_number = db.query(User).filter(User.phone_number == request.phone_number).first()
    if db_phone_number is not None:
        return HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "This phone number already exist")
    return user.user_create(db, request)