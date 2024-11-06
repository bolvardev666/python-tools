import asyncio

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.util import await_only

engine = create_async_engine("sqlite+aiosqlite:///async.db", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    account = Column(String)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, account={self.account!r})"


# async def create_table():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

a_session = AsyncSession(engine,expire_on_commit=False)
async def add_user(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        user = User(name="John", account="john")
        session.add(user)
        await session.commit()

async def select_user(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        user_sql = select(User).where(User.id == 1)
        user = await session.execute(user_sql)
        print(user.all())

async def main():
    async_session = async_sessionmaker(engine)
    # await add_user(async_session)
    await select_user(async_session)
    # await engine.dispose()
    # asyncio.run(create_table())


if __name__ == '__main__':
    asyncio.run(main())
