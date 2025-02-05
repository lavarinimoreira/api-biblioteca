import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from fastapi import status

# Dados para criação de usuário de teste
usuario_data = {
    "nome": "Gabriel Teste",
    "email": "gabriel_teste@example.com",
    "telefone": "123456789",
    "endereco_completo": "Rua de Teste, 123",
    "grupo_politica_id": None,
    "senha_hash": "senhaSegura123"
}

# Dados para criação do livro de teste
livro_data = {
    "titulo": "O Hobbit",
    "autor": "J.R.R. Tolkien",
    "genero": "Fantasia",
    "editora": "HarperCollins",
    "ano_publicacao": 1937,
    "numero_paginas": 310,
    "quantidade_disponivel": 5,
    "isbn": "9780007525492"
}

# Teste para a criação de empréstimo
@pytest.mark.asyncio
async def test_criar_emprestimo(client: AsyncClient):
    # Criar usuario
    response_usuario = await client.post("/usuarios/signup/", json=usuario_data)
    assert response_usuario.status_code == status.HTTP_201_CREATED
    usuario_id = response_usuario.json()["id"]

    # Criar livro
    response_livro = await client.post("/livros/create/", json=livro_data)
    assert response_livro.status_code == status.HTTP_201_CREATED
    livro_id = response_livro.json()["id"]

    # Criar emprestimo
    emprestimo_data = {
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "status": "Ativo"
    }
    response_emprestimo = await client.post("/emprestimos/", json=emprestimo_data)
    assert response_emprestimo.status_code == status.HTTP_201_CREATED
    emprestimo = response_emprestimo.json()
    assert emprestimo["usuario_id"] == usuario_id
    assert emprestimo["livro_id"] == livro_id
    assert emprestimo["status"] == "Ativo"

# Testa a leitura dos empréstimos
@pytest.mark.asyncio
async def test_listar_emprestimos(client: AsyncClient):
    # Criar usuario
    response_usuario = await client.post("/usuarios/signup/", json=usuario_data)
    assert response_usuario.status_code == status.HTTP_201_CREATED
    usuario_id = response_usuario.json()["id"]

    # Criar livro
    response_livro = await client.post("/livros/create/", json=livro_data)
    assert response_livro.status_code == status.HTTP_201_CREATED
    livro_id = response_livro.json()["id"]

    # Criar emprestimo
    emprestimo_data = {
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "status": "Ativo"
    }
    await client.post("/emprestimos/", json=emprestimo_data)
    response = await client.get("/emprestimos/")
    assert response.status_code == status.HTTP_200_OK
    emprestimos = response.json()
    assert isinstance(emprestimos, list)
    assert len(emprestimos) > 0

# Teste para leitura de um empréstimo a partir de seu id
@pytest.mark.asyncio
async def test_obter_emprestimo_por_id(client: AsyncClient):
    # Criar usuario
    response_usuario = await client.post("/usuarios/signup/", json=usuario_data)
    usuario_id = response_usuario.json()["id"]

    # Criar livro
    response_livro = await client.post("/livros/create/", json=livro_data)
    livro_id = response_livro.json()["id"]

    # Criar emprestimo
    emprestimo_data = {
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "status": "Ativo"
    }
    response_emprestimo = await client.post("/emprestimos/", json=emprestimo_data)
    emprestimo_id = response_emprestimo.json()["id"]

    # Obter emprestimo
    response = await client.get(f"/emprestimos/{emprestimo_id}")
    assert response.status_code == status.HTTP_200_OK
    emprestimo = response.json()
    assert emprestimo["id"] == emprestimo_id

# Teste para renovação de empréstimo
@pytest.mark.asyncio
async def test_renovar_emprestimo(client: AsyncClient):
    # Criar usuario
    response_usuario = await client.post("/usuarios/signup/", json=usuario_data)
    usuario_id = response_usuario.json()["id"]

    # Criar livro
    response_livro = await client.post("/livros/create/", json=livro_data)
    livro_id = response_livro.json()["id"]

    # Criar emprestimo
    emprestimo_data = {
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "status": "Ativo"
    }
    response_emprestimo = await client.post("/emprestimos/", json=emprestimo_data)
    emprestimo_id = response_emprestimo.json()["id"]

     # Realizar até 3 renovações permitidas
    for i in range(1, 4):  # 1ª, 2ª e 3ª renovação
        response_renovacao = await client.put(f"/emprestimos/{emprestimo_id}", json={"status": "Renovado"})
        assert response_renovacao.status_code == status.HTTP_200_OK
        emprestimo_renovado = response_renovacao.json()
        assert emprestimo_renovado["numero_renovacoes"] == i

    # Tentar a 4ª renovação, que deve ser negada
    response_renovacao_negada = await client.put(f"/emprestimos/{emprestimo_id}", json={"status": "Renovado"})
    assert response_renovacao_negada.status_code == status.HTTP_400_BAD_REQUEST

# Teste para devolução de livro
@pytest.mark.asyncio
async def test_devolver_emprestimo(client: AsyncClient):
    # Criar usuario
    response_usuario = await client.post("/usuarios/signup/", json=usuario_data)
    usuario_id = response_usuario.json()["id"]

    # Criar livro
    response_livro = await client.post("/livros/create/", json=livro_data)
    livro_id = response_livro.json()["id"]

    # Criar emprestimo
    emprestimo_data = {
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "status": "Ativo"
    }
    response_emprestimo = await client.post("/emprestimos/", json=emprestimo_data)
    emprestimo_id = response_emprestimo.json()["id"]

    # Atualizando o status para devolução
    response_devolucao = await client.put(f"/emprestimos/{emprestimo_id}", json={"status": "Devolvido"})
    assert response_devolucao.status_code == status.HTTP_200_OK
    emprestimo_devolvido = response_devolucao.json()
    assert emprestimo_devolvido["status"] == "Devolvido"

# Teste para deletar empréstimo
@pytest.mark.asyncio
async def test_deletar_emprestimo(client: AsyncClient):
    # Criar usuario
    response_usuario = await client.post("/usuarios/signup/", json=usuario_data)
    usuario_id = response_usuario.json()["id"]

    # Criar livro
    response_livro = await client.post("/livros/create/", json=livro_data)
    livro_id = response_livro.json()["id"]

    # Criar emprestimo
    emprestimo_data = {
        "usuario_id": usuario_id,
        "livro_id": livro_id,
        "status": "Ativo"
    }
    response_emprestimo = await client.post("/emprestimos/", json=emprestimo_data)
    emprestimo_id = response_emprestimo.json()["id"]

    # Deletar emprestimo
    response_delete = await client.delete(f"/emprestimos/{emprestimo_id}")
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que o emprestimo foi deletado
    response_verificar = await client.get(f"/emprestimos/{emprestimo_id}")
    assert response_verificar.status_code == status.HTTP_404_NOT_FOUND