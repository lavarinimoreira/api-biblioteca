import pytest
from httpx import AsyncClient

# Dados para criação de usuário de teste
usuario_data = {
    "nome": "Gabriel Teste",
    "email": "gabriel_teste@example.com",
    "telefone": "123456789",
    "endereco_completo": "Rua de Teste, 123",
    "grupo_politica_id": None,
    "senha_hash": "senhaSegura123"
}

# Teste para criar um novo usuário
@pytest.mark.asyncio
async def test_criar_usuario(client: AsyncClient):
    response = await client.post("/auth/", json=usuario_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == usuario_data["nome"]
    assert data["email"] == usuario_data["email"]

@pytest.mark.asyncio
async def test_criar_usuario_email_duplicado(client: AsyncClient):
    # Primeiro, cria o usuário
    await client.post("/auth/", json=usuario_data)

    # Tenta criar novamente com o mesmo email
    response = await client.post("/auth/", json=usuario_data)

    assert response.status_code == 400
    assert response.json()["detail"] == f"O email fornecido já está cadastrado."



# Teste para listar usuários
@pytest.mark.asyncio
async def test_listar_usuarios(client: AsyncClient):
    # Cria um usuário para garantir que há pelo menos um
    await client.post("/auth/", json=usuario_data)
    
    response = await client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

# Teste para obter usuário por ID
@pytest.mark.asyncio
async def test_obter_usuario_por_id(client: AsyncClient):
    # Cria o usuário primeiro
    response_criar = await client.post("/auth/", json=usuario_data)
    usuario_id = response_criar.json()["id"]

    # Busca o usuário pelo ID
    response = await client.get(f"/usuarios/{usuario_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario_id
    assert data["email"] == usuario_data["email"]

# Teste para obter usuário inexistente
@pytest.mark.asyncio
async def test_obter_usuario_inexistente(client: AsyncClient):
    response = await client.get("/usuarios/9999")  # ID que não existe
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"

# Teste para atualizar usuário
@pytest.mark.asyncio
async def test_atualizar_usuario(client: AsyncClient):
    # Cria o usuário
    response_criar = await client.post("/auth/", json=usuario_data)
    usuario_id = response_criar.json()["id"]

    # Dados para atualização
    update_data = {
        "nome": "Gabriel Atualizado",
        "telefone": "987654321"
    }

    # Atualiza o usuário
    response = await client.put(f"/usuarios/update/{usuario_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Gabriel Atualizado"
    assert data["telefone"] == "987654321"

# Teste para deletar usuário
@pytest.mark.asyncio
async def test_deletar_usuario(client: AsyncClient):
    # Cria o usuário
    response_criar = await client.post("/auth/", json=usuario_data)
    usuario_id = response_criar.json()["id"]

    # Deleta o usuário
    response = await client.delete(f"/usuarios/delete/{usuario_id}")
    assert response.status_code == 204

    # Verifica se o usuário foi deletado
    response_verificar = await client.get(f"/usuarios/{usuario_id}")
    assert response_verificar.status_code == 404
    assert response_verificar.json()["detail"] == "Usuário não encontrado"
