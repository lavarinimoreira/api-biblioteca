from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import necessário para consultas

from app.database import get_db
from app.models.models import Livro
from app.schemas.book import LivroCreate, LivroRead  # Importando o novo schema para leitura

router = APIRouter()


"""---------------------------------------------------------------------------
CREATE routers
"""
@router.post("/livro/create/", status_code=status.HTTP_201_CREATED, response_model=LivroCreate)
async def create_livro(livro: LivroCreate, db: AsyncSession = Depends(get_db)):
    db_livro = Livro(
        titulo=livro.titulo,
        autor=livro.autor,
        genero=livro.genero,
        editora=livro.editora,
        ano_publicacao=livro.ano_publicacao,
        numero_paginas=livro.numero_paginas,
        quantidade_disponivel=livro.quantidade_disponivel,
        isbn=livro.isbn
    )
    db.add(db_livro)
    await db.commit()
    await db.refresh(db_livro)
    return db_livro



"""---------------------------------------------------------------------------
READ routers
"""
@router.get("/livro", status_code=status.HTTP_200_OK, response_model=list[LivroRead])
async def read_livros(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Livro))
    livros = result.scalars().all()
    return livros
