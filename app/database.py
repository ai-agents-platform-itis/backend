from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


def form_db_url() -> str:
    return URL.create(
        drivername=settings.db.driver,
        username=settings.db.user,
        password=settings.db.password,
        host=settings.db.host,
        port=settings.db.port,
        database=settings.db.name,
    ).render_as_string(hide_password=False)


engine = create_async_engine(
    form_db_url(),
    echo=settings.app.debug,
    future=True,
    pool_size=20,  # Максимальное количество соединений в пуле
    max_overflow=10,  # Дополнительные соединения сверх pool_size
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
