import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

async def create_access_token(data:dict,expires_minutes:int = 15):
    to_encode = data.copy()
    expires = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp":expires})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def create_refresh_token(data:dict, expires_days:int = 7):
    to_encode = data.copy()
    expires = datetime.now() + timedelta(days=expires_days)
    to_encode.update({"exp":expires})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def decode_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Token invalido")
    
async def is_token_near_expiry(payload:dict,threshold_minutes:int = 2):
    exp = datetime.fromtimestamp(payload["exp"])
    remainig = datetime.now() - exp
    return remainig < timedelta(minutes=threshold_minutes)