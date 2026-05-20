from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.database.config import Config


Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None

    def init(self):
        self._engine = create_async_engine(
            Config.DB_CONFIG,
            echo=True,
            future=True
        )

        self._session = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self._engine.dispose()

    async def get_db(self):
        async with self._session() as session:
            yield session


db = AsyncDatabaseSession()
db.init()