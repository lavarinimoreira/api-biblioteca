from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


DATABASE_URL = "postgresql+asyncpg://dev_gabriel:university@localhost:5432/biblioteca"

# Criação do async engine
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

# Criação do async session factory
AsyncSessionLocal: AsyncSession = sessionmaker(autocommit=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# Função para obter sessão do banco de dados
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session