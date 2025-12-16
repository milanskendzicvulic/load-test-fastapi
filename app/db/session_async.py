from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.settings import settings

async_engine = create_async_engine(
    url=settings.POSTGRES_DSN_ASYNC,
    pool_pre_ping=True,
    echo=False, 
    pool_size=10,  
    max_overflow=12,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()