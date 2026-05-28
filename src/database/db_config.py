from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.database.config import Config


Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(
            Config.DB_CONFIG,
            future=True,
            echo=True
        )

        session_local = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

        self._session = session_local()


db = AsyncDatabaseSession()
db.init()


async def get_db():
    try:
        yield db
    finally:
        pass