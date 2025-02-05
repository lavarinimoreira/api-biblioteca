import pytest
from fastapi import status


"""---------------------------------------------------------------------------
CREATE tests
"""
@pytest.mark.asyncio
async def test_create_livro(client):
    response = await client.post("/livros/create/", json={
        "titulo": "O Hobbit",
        "autor": "J.R.R. Tolkien",
        "genero": "Fantasia",
        "editora": "HarperCollins",
        "ano_publicacao": 1937,
        "numero_paginas": 310,
        "quantidade_disponivel": 5,
        "isbn": "9780007525492"
    })

    assert response.status_code == status.HTTP_201_CREATED  
    data = response.json()
    assert data["titulo"] == "O Hobbit"
    assert data["autor"] == "J.R.R. Tolkien"


import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_livro_quantidade_negativa(client):
    response = await client.post("/livros/create/", json={
        "titulo": "Livro com Quantidade Negativa",
        "autor": "Autor Teste",
        "genero": "Ficção",
        "editora": "Editora Teste",
        "ano_publicacao": 2025,
        "numero_paginas": 250,
        "quantidade_disponivel": -3,  # Valor negativo que deve ser rejeitado
        "isbn": "9780000000001"
    })

    # O código esperado é 422 Unprocessable Entity
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Verificar se a mensagem de erro está relacionada à quantidade negativa
    error_detail = response.json()
    assert error_detail["detail"][0]["loc"] == ["body", "quantidade_disponivel"]
    assert error_detail["detail"][0]["msg"] == "Input should be greater than or equal to 0"
    assert error_detail["detail"][0]["type"] == "greater_than_equal"


"""---------------------------------------------------------------------------
READ tests
"""
@pytest.mark.asyncio
async def test_read_livros(client):
    # Primeiro, cria um livro para garantir que temos algo no banco
    await client.post("/livros/create/", json={
        "titulo": "Dom Quixote",
        "autor": "Miguel de Cervantes",
        "genero": "Distopia",
        "editora": "Francisco de Robles",
        "ano_publicacao": 1605,
        "numero_paginas": 328,
        "quantidade_disponivel": 3,
        "isbn": "9786584956261"
    })

    # Agora testa o GET /livros
    response = await client.get("/livros/")
    
    assert response.status_code == status.HTTP_200_OK
    livros = response.json()
    
    assert isinstance(livros, list)  # Verifica se o retorno é uma lista
    assert len(livros) >= 1  # Deve haver pelo menos um livro cadastrado
    
    # Verifica se o livro 'Dom Quixote' está na lista
    encontrado = any(livro["titulo"] == "Dom Quixote" and livro["autor"] == "Miguel de Cervantes" for livro in livros)
    assert encontrado


"""---------------------------------------------------------------------------
UPDATE tests
"""
@pytest.mark.asyncio
async def test_update_livro(client):
    # Criação do livro
    create_response = await client.post("/livros/create/", json={
        "titulo": "1984",
        "autor": "George Orwell",
        "genero": "Distopia",
        "editora": "Secker & Warburg",
        "ano_publicacao": 1949,
        "numero_paginas": 328,
        "quantidade_disponivel": 4,
        "isbn": "9780451524935"
    })
    
    assert create_response.status_code == status.HTTP_201_CREATED
    livro_criado = create_response.json()
    livro_id = livro_criado["id"]

    # Verificar se o livro existe após criação
    get_response = await client.get(f"/livros/{livro_id}")
    assert get_response.status_code == status.HTTP_200_OK, f"Livro não encontrado após criação: {get_response.json()}"

    # Atualizar o livro (rota atualizada para '/livro/update/{livro_id}')
    update_response = await client.put(f"/livros/update/{livro_id}", json={
        "titulo": "1984 - Edição Atualizada",
        "quantidade_disponivel": 10
    })

    assert update_response.status_code == status.HTTP_200_OK, f"Erro na atualização: {update_response.json()}"
    livro_atualizado = update_response.json()

    # Verificações para garantir que os campos foram atualizados corretamente
    assert livro_atualizado["titulo"] == "1984 - Edição Atualizada"
    assert livro_atualizado["quantidade_disponivel"] == 10

    # Verificação para garantir que os campos não atualizados permanecem inalterados
    assert livro_atualizado["autor"] == "George Orwell"
    assert livro_atualizado["isbn"] == "9780451524935"



"""---------------------------------------------------------------------------
DELETE tests
"""
@pytest.mark.asyncio
async def test_delete_livro(client):
    # Primeiro, cria um livro para poder deletá-lo
    create_response = await client.post("/livros/create/", json={
        "titulo": "Livro para Deletar",
        "autor": "Autor Teste",
        "genero": "Teste",
        "editora": "Editora Teste",
        "ano_publicacao": 2020,
        "numero_paginas": 200,
        "quantidade_disponivel": 1,
        "isbn": "1234567890123"
    })

    assert create_response.status_code == status.HTTP_201_CREATED
    livro_criado = create_response.json()
    livro_id = livro_criado["id"]

    # Agora deleta o livro criado
    delete_response = await client.delete(f"/livros/delete/{livro_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Tenta buscar o livro deletado para garantir que ele foi removido
    get_response = await client.get(f"/livros/{livro_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
