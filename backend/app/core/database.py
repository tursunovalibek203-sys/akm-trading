from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


def _make_engine():
    url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    connect_args: dict = {}
    # asyncpg accepts ssl as bool/SSLContext — not as a URL string param
    for param in ("ssl=require", "ssl=true", "ssl=verify-full"):
        url = url.replace(f"?{param}", "").replace(f"&{param}", "")
    if "neon.tech" in url or settings.ENVIRONMENT == "production":
        connect_args["ssl"] = True
    return create_async_engine(
        url,
        pool_size=5,
        max_overflow=2,
        echo=settings.DEBUG,
        connect_args=connect_args,
    )


engine = _make_engine()

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
