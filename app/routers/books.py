from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import necessário para consultas

from app.database import get_db
from app.models.models import Livro
from app.schemas.book import LivroCreate, LivroRead, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


"""---------------------------------------------------------------------------
CREATE routers
"""
@router.post("/create/", status_code=status.HTTP_201_CREATED, response_model=LivroRead)
async def create_livro(livro: LivroCreate, db: AsyncSession = Depends(get_db)):
    db_livro = Livro(
        titulo=livro.titulo,
        autor=livro.autor,
        genero=livro.genero,
        editora=livro.editora,
        ano_publicacao=livro.ano_publicacao,
        numero_paginas=livro.numero_paginas,
        quantidade_disponivel=livro.quantidade_disponivel,
        isbn=livro.isbn,
        # data_criacao=datetime.now(timezone.utc),       # O Banco de dados resolverá automaticamente.
        # data_atualizacao=datetime.now(timezone.utc)    # 
    )
    db.add(db_livro)
    await db.commit()
    await db.refresh(db_livro)
    return db_livro



"""---------------------------------------------------------------------------
READ routers
"""
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[LivroRead])
async def read_livros(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Livro))
    livros = result.scalars().all()
    return livros


@router.get("/{livro_id}", response_model=LivroRead, status_code=status.HTTP_200_OK)
async def get_livro(livro_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Livro).where(Livro.id == livro_id))
    livro = result.scalars().first()

    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    return livro

"""---------------------------------------------------------------------------
UPDATE routers
"""
@router.put("/update/{livro_id}", response_model=LivroRead)
async def atualizar_livro(livro_id: int, livro_update: LivroUpdate = Body(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Livro).where(Livro.id == livro_id))
    livro = result.scalars().first()

    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    for campo, valor in livro_update.model_dump(exclude_unset=True).items():
        setattr(livro, campo, valor)

    # livro.data_atualizacao = datetime.now(timezone.utc) # O banco de Dados lidará com a atualização automaticamente.
    await db.commit()
    await db.refresh(livro)

    return livro


"""---------------------------------------------------------------------------
DELETE routers
"""
@router.delete("/delete/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_livro(livro_id: int, db: AsyncSession = Depends(get_db)):
    # Verificar se o livro existe
    result = await db.execute(select(Livro).where(Livro.id == livro_id))
    livro = result.scalars().first()

    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Deletar o livro
    await db.delete(livro)
    await db.commit()

    return None  # Retorno vazio para 204 No Content