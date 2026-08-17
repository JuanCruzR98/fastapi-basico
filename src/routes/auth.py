from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, conint,constr
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from modules.user import User,UserResponse
from controllers.auth import signup, login
from database.config import get_db
import re


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Debe contener al menos una letra minúscula")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Debe contener al menos una letra mayúscula")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Debe contener al menos un número")
    if not re.search(r"[@$!%*?&]", password):
        raise HTTPException(status_code=400, detail="Debe contener al menos un símbolo @$!%*?&")
    return password


class UserSignModel(BaseModel):
    email:EmailStr
    password:str = Depends(validate_password)
    
class UserSingUpModel(BaseModel):
    username:str 
    password: str = Depends(validate_password)
    email: EmailStr



router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/sign")
async def sign_in(user:UserSingUpModel,db: Session = Depends(get_db)):
    print(user)
    return await signup(user.email,user.username,user.password,db)

@router.post("/login", response_model=UserResponse)
async def log_in(user:UserSignModel,db: AsyncSession = Depends(get_db)):
    return await login(email=user.email,password=user.password,db=db)
