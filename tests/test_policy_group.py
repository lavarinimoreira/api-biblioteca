import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_criar_grupo_politica(client: AsyncClient):
    response = await client.post("/grupos_politica/", json={"nome": "Admin"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == "Admin"
    assert "id" in data

@pytest.mark.asyncio
async def test_listar_grupos_politica(client: AsyncClient):
    await client.post("/grupos_politica/", json={"nome": "Admin"})
    await client.post("/grupos_politica/", json={"nome": "Moderador"})
    response = await client.get("/grupos_politica/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_obter_grupo_politica(client: AsyncClient):
    # Cria um grupo para garantir que ele existe
    response = await client.post("/grupos_politica/", json={"nome": "Moderador"})
    grupo_id = response.json()["id"]

    # Busca o grupo criado
    response = await client.get(f"/grupos_politica/{grupo_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == grupo_id
    assert data["nome"] == "Moderador"

@pytest.mark.asyncio
async def test_atualizar_grupo_politica(client: AsyncClient):
    # Cria um grupo para atualizar
    response = await client.post("/grupos_politica/", json={"nome": "Usuario Comum"})
    grupo_id = response.json()["id"]

    # Atualiza o nome do grupo
    response = await client.put(f"/grupos_politica/update/{grupo_id}", json={"nome": "Usuario Atualizado"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == grupo_id
    assert data["nome"] == "Usuario Atualizado"

@pytest.mark.asyncio
async def test_deletar_grupo_politica(client: AsyncClient):
    # Cria um grupo para deletar
    response = await client.post("/grupos_politica/", json={"nome": "Grupo Temporario"})
    grupo_id = response.json()["id"]

    # Deleta o grupo criado
    response = await client.delete(f"/grupos_politica/{grupo_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verifica se o grupo foi realmente deletado
    response = await client.get(f"/grupos_politica/{grupo_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
