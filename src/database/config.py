import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
load_dotenv()

DATABASE_URL = (
    f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
