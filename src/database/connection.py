import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncConnection
from dotenv import load_dotenv, find_dotenv
import logging
# from os import getenv
# from urllib.parse import urlparse
# from tenacity import retry, stop_after_attempt, wait_fixed
from database.models import table_registry

load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# db_params = urlparse(getenv("DATABASE_URL"))
engine = None

# @retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
async def get_engine():
    """Cria engine com tentativas de reconexão"""
   
    # logger.info(f"Tentando conectar ao banco de dados: {db_params.hostname}")
    
    # db_url = f"postgresql+asyncpg://{db_params.username}:{db_params.password}@{db_params.hostname}{db_params.path}?ssl=require"
    db_url = "sqlite+aiosqlite:///data/app_database.db"
    
    engine = create_async_engine(
        db_url,
        echo=True,
        future=True,
        pool_pre_ping=True
    )

    # Testa a conexão
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    
    logger.info("Conexão com o banco de dados estabelecida com sucesso!")
    return engine


async def initial_inserts(bind: AsyncConnection):
    from os import path   
    import re
    from sqlalchemy import text
    from database.models import PessoaGenero
    from sqlalchemy.exc import SQLAlchemyError

    try:        
        data_path = "data"
        # Estados
        # Caminho do script sql para carga
        db_file = path.join(data_path, "tab_states.sql")        
        with open(db_file, "r", encoding="utf-8") as f:
            statements = re.split(r";\s*$", f.read().strip(), flags=re.MULTILINE)
            for stmt in statements:
                if stmt:
                    await bind.execute(text(stmt))
        
        # Municicipios
        # Caminho do script sql para carga
        db_file = path.join(data_path, "tab_cities.sql")        
        with open(db_file, "r", encoding="utf-8") as f:
            statements = re.split(r";\s*$", f.read().strip(), flags=re.MULTILINE)
            for stmt in statements:
                if stmt:
                    await bind.execute(text(stmt))

        # PessoaGenero        
        gen_masc = {'description':'Masculino'}
        gen_fem  = {'description':'Feminino'}
        await bind.execute(PessoaGenero.insert(), [gen_masc, gen_fem])
        

    except SQLAlchemyError as e:        
        await bind.rollback()
        logger.error(f"Erro ao popular o database com os dados iniciais: {e.__repr__()}")
        raise
    else:
        await bind.commit()


async def init_db():
    from sqlalchemy import select
    from database.models import PessoaGenero

    global engine
    
    try:
        engine = await get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.create_all)
            
            # Check if initial inserts are necessary
            result = await conn.execute(select(PessoaGenero.id).limit(1))
            check_ins = result.one_or_none()
            if check_ins is None:
                await initial_inserts(conn)
                
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