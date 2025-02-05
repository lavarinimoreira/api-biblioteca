from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

import pytest_asyncio
import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.models import Base
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app 
from sqlalchemy.pool import NullPool


TEST_DATABASE_URL = "postgresql+asyncpg://dev_gabriel:university@localhost:5432/biblioteca_test"

test_engine: AsyncEngine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    poolclass=NullPool  # Desativa o pool de conexões
)

TestAsyncSessionLocal: AsyncSession = sessionmaker(
    autocommit=False,
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Configura o banco de dados para criar e dropar tabelas para os testes
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Garante que não há resíduos de testes anteriores
        await conn.run_sync(Base.metadata.create_all)  # Criação das tabelas
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Limpeza após os testes

# Fixture que cria e gerencia a transação do banco para cada teste
@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with test_engine.connect() as connection:
        # Inicia uma transação
        async with connection.begin() as transaction:
            session = TestAsyncSessionLocal(bind=connection)
            try:
                yield session  # Passa a sessão para o teste
            finally:
                await session.close()
                await transaction.rollback()  # Faz rollback para isolar o teste

# Fixture do cliente HTTP, sobrescrevendo a dependência do banco
@pytest_asyncio.fixture(scope="function")
async def client(async_session):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()
