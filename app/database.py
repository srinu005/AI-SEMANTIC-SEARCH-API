from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+psycopg://admin:password@db:5432/semantic_search"

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Dependency to get DB session in FastAPI
async def get_db():
    async with async_session() as session:
        yield session