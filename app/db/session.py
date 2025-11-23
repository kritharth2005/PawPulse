from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Create the Async Engine
# This connects to the URL we set in .env
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # This logs all SQL queries to the terminal (Great for debugging)
    future=True
)

# 2. Create the Session Factory
# We don't open a new connection every time; we ask this factory for one.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. Dependency Injection (The 'get_db' function)
# FastAPI uses this to give every request its own database session.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()