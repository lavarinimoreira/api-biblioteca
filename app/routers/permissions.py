from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.permission import Permissao as PermissaoModel
from app.schemas.permission import PermissaoCreate, PermissaoOut, PermissaoUpdate
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/permissoes", tags=["Permissoes"])

@router.post("/", response_model=PermissaoOut, status_code=status.HTTP_201_CREATED)
async def criar_permissao(permissao: PermissaoCreate, db: AsyncSession = Depends(get_db)):
    nova_permissao = PermissaoModel(
        nome=permissao.nome,
        descricao=permissao.descricao,
        namespace=permissao.namespace
    )
    db.add(nova_permissao)
    try:
        await db.commit()
        await db.refresh(nova_permissao)
        return nova_permissao
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permissão já existe.")

@router.get("/", response_model=list[PermissaoOut])
async def listar_permissoes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PermissaoModel))
    permissoes = result.scalars().all()
    return permissoes

@router.get("/{permissao_id}", response_model=PermissaoOut)
async def obter_permissao(permissao_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PermissaoModel).filter(PermissaoModel.id == permissao_id))
    permissao = result.scalars().first()
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")
    return permissao

@router.put("/{permissao_id}", response_model=PermissaoOut)
async def atualizar_permissao(permissao_id: int, permissao_update: PermissaoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PermissaoModel).filter(PermissaoModel.id == permissao_id))
    permissao = result.scalars().first()
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")

    permissao.nome = permissao_update.nome
    permissao.descricao = permissao_update.descricao
    permissao.namespace = permissao_update.namespace
    permissao.data_atualizacao = datetime.now()

    try:
        await db.commit()
        await db.refresh(permissao)
        return permissao
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permissão já existe.")

@router.delete("/{permissao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_permissao(permissao_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PermissaoModel).filter(PermissaoModel.id == permissao_id))
    permissao = result.scalars().first()
    if not permissao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissão não encontrada.")

    await db.delete(permissao)
    await db.commit()
    return None
