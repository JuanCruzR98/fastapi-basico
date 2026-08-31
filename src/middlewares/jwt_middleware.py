from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer
from helpers.jwt_handler import decode_token,is_token_near_expiry

class JWTMiddleware(HTTPBearer):
    async def __call__(self, request:Request):
        credentials = await super().__call__(request)
        token = credentials.credentials
        payload = await decode_token(token)
        if await is_token_near_expiry(payload):
            raise HTTPException(status_code=401,detail="El token esta por expirar")
        request.state.user = payload
        return payload