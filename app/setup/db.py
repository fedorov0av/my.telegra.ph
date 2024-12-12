import asyncio
import contextlib
from typing import Any, AsyncIterator
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.orm import close_all_sessions, sessionmaker
from sqlalchemy.exc import ArgumentError
from sqlalchemy import create_engine

from app.db.models import Base
from ..config import SqliteDB, PostgresDB, DATABASE_DIR


Database = SqliteDB | PostgresDB

async def close_db():
    close_all_sessions()
    logger.info("Database closed")


async def dev_init_db(db: Database = PostgresDB.default()) -> async_sessionmaker:
    from sqlalchemy_utils import database_exists, create_database
    #logger.info(f"Initializing Database {db.database}[{db.host}]...")
    engine = create_async_engine(db.url, echo=True)
    #logger.info(database_exists(db.sync_url))
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    
    if not database_exists(db.sync_url):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        engine_sync = create_engine(db.sync_url, echo=True)
        print(engine_sync.url)
        if not DATABASE_DIR.exists():
            DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        Base.metadata.create_all(bind=engine_sync)
        print('4234324324234')

        #create_database(db.sync_url)
        #logger.info(f"Database {db.database}[{db.host}] created")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Database {db.database}[{db.host}] initialized")
    return async_sessionmaker(engine, expire_on_commit=False)


async def init_db(db: Database = PostgresDB.default(), dev: bool = False) -> async_sessionmaker:
    print(dev)
    if dev:
        return await dev_init_db(db)
    logger.info(f"Initializing {db}...")
    engine = create_async_engine(db.url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Database {db} initialized")
    return async_sessionmaker(engine, expire_on_commit=False)





class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_db():
    database = SqliteDB()
    database.path = str(DATABASE_DIR / "app.db")
    await dev_init_db(database)

try:
    sessionmanager = DatabaseSessionManager(str(DATABASE_DIR / "app.db"), {"echo": True})
except:
    asyncio.create_task(create_db())




async def get_db_session():
    async with sessionmanager.session() as session:
        yield session