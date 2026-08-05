from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import settings

async_engine = create_async_engine(
    url=settings.database_url,
    pool_pre_ping=settings.database_pool_pre_ping,
    pool_recycle=settings.database_pool_recycle,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
