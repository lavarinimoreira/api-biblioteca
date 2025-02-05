import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_criar_permissao(client: AsyncClient):
    response = await client.post("/permissoes/", json={"nome": "criar_usuario", "descricao": "Permite criar usuários", "namespace": "usuarios"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == "criar_usuario"
    assert data["descricao"] == "Permite criar usuários"
    assert data["namespace"] == "usuarios"
    assert "id" in data

@pytest.mark.asyncio
async def test_listar_permissoes(client: AsyncClient):
    await client.post("/permissoes/", json={"nome": "criar_usuario", "descricao": "Permite criar usuários", "namespace": "usuarios"})
    response = await client.get("/permissoes/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_obter_permissao(client: AsyncClient):
    response = await client.post("/permissoes/", json={"nome": "editar_usuario", "descricao": "Permite editar usuários", "namespace": "usuarios"})
    permissao_id = response.json()["id"]

    response = await client.get(f"/permissoes/{permissao_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == permissao_id
    assert data["nome"] == "editar_usuario"

@pytest.mark.asyncio
async def test_atualizar_permissao(client: AsyncClient):
    response = await client.post("/permissoes/", json={"nome": "deletar_usuario", "descricao": "Permite deletar usuários", "namespace": "usuarios"})
    permissao_id = response.json()["id"]

    response = await client.put(f"/permissoes/{permissao_id}", json={"nome": "remover_usuario", "descricao": "Permite remover usuários", "namespace": "usuarios"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == permissao_id
    assert data["nome"] == "remover_usuario"

@pytest.mark.asyncio
async def test_deletar_permissao(client: AsyncClient):
    response = await client.post("/permissoes/", json={"nome": "visualizar_logs", "descricao": "Permite visualizar logs", "namespace": "logs"})
    permissao_id = response.json()["id"]

    response = await client.delete(f"/permissoes/{permissao_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f"/permissoes/{permissao_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
