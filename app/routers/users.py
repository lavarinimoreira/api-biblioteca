from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Usuario as UsuarioModel
from app.schemas.user import UsuarioCreate, UsuarioOut, UsuarioUpdate
from app.database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


"""---------------------------------------------------------------------------
CREATE routers
"""
# Criar um novo usuário
@router.post("/signup/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    novo_usuario = UsuarioModel(**usuario.model_dump())
    db.add(novo_usuario)
    try:
        await db.commit()
        await db.refresh(novo_usuario)
    except IntegrityError as e:
        await db.rollback()
        if 'email' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email '{usuario.email}' já está cadastrado.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar o usuário.")
    return novo_usuario

   


"""---------------------------------------------------------------------------
READ routers
"""
# Listar todos os usuários
@router.get("/", response_model=list[UsuarioOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UsuarioModel))
    return result.scalars().all()

# Obter usuário por ID
@router.get("/{usuario_id}", response_model=UsuarioOut)
async def obter_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await db.get(UsuarioModel, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario


"""---------------------------------------------------------------------------
UPDATE routers
"""
# Atualizar usuário
@router.put("/update/{usuario_id}", response_model=UsuarioOut)
async def atualizar_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: AsyncSession = Depends(get_db)):
    usuario = await db.get(UsuarioModel, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    for key, value in usuario_update.model_dump(exclude_unset=True).items():
        setattr(usuario, key, value)
    
    await db.commit()
    await db.refresh(usuario)
    return usuario


"""---------------------------------------------------------------------------
DELETE routers
"""
# Deletar usuário
@router.delete("/delete/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await db.get(UsuarioModel, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    await db.delete(usuario)
    await db.commit()
    return None
