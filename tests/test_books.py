import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_livro(client):
    response = await client.post("/livro/create/", json={
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

@pytest.mark.asyncio
async def test_read_livros(client):
    # Primeiro, cria um livro para garantir que temos algo no banco
    await client.post("/livro/create/", json={
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
    response = await client.get("/livro")
    
    assert response.status_code == status.HTTP_200_OK
    livros = response.json()
    
    assert isinstance(livros, list)  # Verifica se o retorno é uma lista
    assert len(livros) >= 1  # Deve haver pelo menos um livro cadastrado
    
    # Verifica se o livro 'Dom Quixote' está na lista
    encontrado = any(livro["titulo"] == "Dom Quixote" and livro["autor"] == "Miguel de Cervantes" for livro in livros)
    assert encontrado

