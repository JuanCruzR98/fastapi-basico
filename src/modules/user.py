import uuid
from sqlalchemy import Column,Integer,String,LargeBinary,BINARY
from database.config import Base
from pydantic import BaseModel

class User(Base):
    __tablename__="usuarios"
    
    idusuarios = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String(45),unique=True,index=True)
    password = Column(LargeBinary)
    email=Column(String(45),unique=True)
    uuid= Column(BINARY(16),default=lambda:uuid.uuid4().bytes)
    
    
    
class UserResponse(BaseModel):
    uuid:str
    username:str
    email:str

    class Config:
        orm_mode = True