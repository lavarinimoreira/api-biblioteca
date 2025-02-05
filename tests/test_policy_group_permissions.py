import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_adicionar_permissao_ao_grupo(client: AsyncClient):
    # Criar um grupo e uma permissao para associar
    grupo_response = await client.post("/grupos_politica/", json={"nome": "Admin"})
    permissao_response = await client.post("/permissoes/", json={"nome": "criar_usuario", "descricao": "Permite criar usuários", "namespace": "usuarios"})

    grupo_id = grupo_response.json()["id"]
    permissao_id = permissao_response.json()["id"]

    # Associar permissao ao grupo
    response = await client.post("/grupo_politica_permissoes/", json={"grupo_politica_id": grupo_id, "permissao_id": permissao_id})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["grupo_politica_id"] == grupo_id
    assert data["permissao_id"] == permissao_id

@pytest.mark.asyncio
async def test_listar_permissoes_grupo(client: AsyncClient):
    # Criar um grupo e uma permissão para garantir que há dados
    grupo_response = await client.post("/grupos_politica/", json={"nome": "Teste Grupo"})
    permissao_response = await client.post("/permissoes/", json={
        "nome": "acessar_dashboard", 
        "descricao": "Permite acessar o dashboard", 
        "namespace": "dashboard"
    })

    grupo_id = grupo_response.json()["id"]
    permissao_id = permissao_response.json()["id"]

    # Associar permissão ao grupo
    await client.post("/grupo_politica_permissoes/", json={
        "grupo_politica_id": grupo_id,
        "permissao_id": permissao_id
    })

    # Listar as permissões do grupo
    response = await client.get("/grupo_politica_permissoes/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Agora deve ter pelo menos uma associação


@pytest.mark.asyncio
async def test_remover_permissao_do_grupo(client: AsyncClient):
    # Criar um grupo e uma permissao para associar e depois remover
    grupo_response = await client.post("/grupos_politica/", json={"nome": "Moderador"})
    permissao_response = await client.post("/permissoes/", json={"nome": "editar_conteudo", "descricao": "Permite editar conteúdos", "namespace": "conteudo"})

    grupo_id = grupo_response.json()["id"]
    permissao_id = permissao_response.json()["id"]

    # Associar permissao ao grupo
    await client.post("/grupo_politica_permissoes/", json={"grupo_politica_id": grupo_id, "permissao_id": permissao_id})

    # Remover a permissao do grupo
    response = await client.delete(f"/grupo_politica_permissoes/?grupo_politica_id={grupo_id}&permissao_id={permissao_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Confirmar que a permissao foi removida
    response = await client.get("/grupo_politica_permissoes/")
    data = response.json()
    assert {"grupo_politica_id": grupo_id, "permissao_id": permissao_id} not in data