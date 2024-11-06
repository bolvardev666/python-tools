from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.ext.declarative import declarative_base
import asyncio


engine = create_async_engine("sqlite+aiosqlite:///example-sqlite3.db",echo=True)
BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    account = Column(String)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

def main():
    asyncio.run(create_table())

if __name__ == '__main__':
    main()