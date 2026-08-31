import bcrypt
import uuid
from fastapi import HTTPException
from fastapi.responses import Response
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from helpers.jwt_handler import create_access_token,create_refresh_token,decode_token
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
    


async def login(email:str,password:str,db:AsyncSession,response:Response):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404,detail="correo no encontrado")
    if not bcrypt.checkpw(password.encode("utf-8"),user.password):
        raise HTTPException(status_code=401, detail="contraseña incorrecta")
    
    access = await create_access_token({"username":user.username,"email":user.email,"uuid":str(uuid.UUID(bytes=user.uuid))})
    refresh = await create_refresh_token({"username":user.username,"email":user.email,"uuid":str(uuid.UUID(bytes=user.uuid))})
    
    userconverted = await to_response(user,access)
    
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7*86400,
        path="/api/auth/refresh"
    )
    
    return userconverted  


async def renew(request:Request):
    print(request.cookies)
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No se proporcionó un token de actualización")
    
    try:
        payload = await decode_token(refresh_token)

    except Exception as e:
        raise HTTPException(status_code=401, detail="Token de actualización inválido")
    
    new_access_token = await create_access_token({"username":payload["username"],"email":payload["email"],"uuid":payload["uuid"]})    
    return {"access_token": new_access_token}

async def to_response(user,access:str):
    return UserResponse(
        idusuarios=user.idusuarios,
        uuid=str(uuid.UUID(bytes=user.uuid)),  # conversión binario → string
        username=user.username,
        email=user.email,
        access_token=access
    )