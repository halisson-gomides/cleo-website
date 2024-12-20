import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv, find_dotenv
import logging
from os import getenv
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_fixed
from database.models import table_registry

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_url = urlparse(getenv("DATABASE_URL"))
engine = None

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
async def get_engine():
    """Cria engine com tentativas de reconexão"""
   
    logger.info(f"Tentando conectar ao banco de dados: {db_url.hostname}")
    
    engine = create_async_engine(
        f"postgresql+asyncpg://{db_url.username}:{db_url.password}@{db_url.hostname}{db_url.path}?ssl=require",
        echo=True,
        future=True,
        pool_pre_ping=True
    )

    # Testa a conexão
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    
    logger.info("Conexão com o banco de dados estabelecida com sucesso!")
    return engine


async def init_db():
    global engine
    try:
        engine = await get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.create_all)
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if engine is None:
        raise Exception("Database não foi inicializado. Chame init_db() primeiro.")
    
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()