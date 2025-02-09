from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from app.models.policy_group_permission import grupo_politica_permissao
from app.schemas.policy_group_permission import GrupoPoliticaPermissaoCreate, GrupoPoliticaPermissaoOut
from app.database import get_db

router = APIRouter(prefix="/grupo_politica_permissoes", tags=["Grupo Politica Permissoes"])



@router.post("/", response_model=GrupoPoliticaPermissaoOut, status_code=status.HTTP_201_CREATED)
async def adicionar_permissao_ao_grupo(relacao: GrupoPoliticaPermissaoCreate, db: AsyncSession = Depends(get_db)):
    stmt = insert(grupo_politica_permissao).values(
        grupo_politica=relacao.grupo_politica,
        permissao_id=relacao.permissao_id
    )
    try:
        await db.execute(stmt)
        await db.commit()
        return relacao
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao adicionar permissão ao grupo.")

@router.get("/", response_model=list[GrupoPoliticaPermissaoOut])
async def listar_permissoes_grupo(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(grupo_politica_permissao))
    permissoes_grupos = result.fetchall()
    return [{"grupo_politica": row.grupo_politica, "permissao_id": row.permissao_id} for row in permissoes_grupos]

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def remover_permissao_do_grupo(grupo_politica: int, permissao_id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(grupo_politica_permissao).where(
        grupo_politica_permissao.c.grupo_politica == grupo_politica,
        grupo_politica_permissao.c.permissao_id == permissao_id
    )
    result = await db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relacionamento não encontrado.")

    await db.commit()
    return None