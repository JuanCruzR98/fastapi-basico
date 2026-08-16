import bcrypt
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.user import User, UserResponse

async def signup(email:str,username:str,password:str,db:AsyncSession):
    result = await db.execute(select(User).filter(User.email==email))
    existingdb = result.scalars().first()
    if existingdb:
        raise HTTPException(status_code=409,detail="correo se encuentra en uso")
    
    hashed = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    new_user = User(email=email,username=username,password=hashed)
    print(new_user)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    


async def login(email:str,password:str,db:AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404,detail="correo no encontrado")
    if not bcrypt.checkpw(password.encode("utf-8"),user.password):
        raise HTTPException(status_code=401, detail="contraseña incorrecta")
    
    return to_response(user)  



def to_response(user):
    return UserResponse(
        idusuarios=user.idusuarios,
        uuid=str(uuid.UUID(bytes=user.uuid)),  # conversión binario → string
        username=user.username,
        email=user.email
    )