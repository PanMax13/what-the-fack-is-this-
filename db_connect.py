from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import Base, User, Project


# TODO: создать 2 сущности: пользователь и проект. У проекта может быть привязано несколько пользователей,
#  у пользователя может быть больше, чем 1 проект

load_dotenv()


engine = create_async_engine('postgresql+asyncpg://maksimpanezha:MyNewPassword@127.0.0.1:5432/maksimpaneza')

MySession = sessionmaker(
    engine, class_=AsyncSession
)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = MySession()

    try:
        yield db
    finally:
        await db.close()

