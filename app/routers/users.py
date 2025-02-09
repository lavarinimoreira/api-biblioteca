from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Usuario as UsuarioModel
from app.schemas.user import UsuarioCreate, UsuarioOut, UsuarioUpdate
from app.database import get_db
from app.services.security import get_current_user, bcrypt_context

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


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
async def atualizar_usuario(
    usuario_id: int, 
    usuario_update: UsuarioUpdate, 
    db: AsyncSession = Depends(get_db), 
    user: dict = Depends(get_current_user)  # Garante que a requisição tenha um usuário autenticado
):
    # Verifica se o usuário autenticado está tentando atualizar outro usuário
    if user["id"] != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permissão negada"
        )
    
    # Busca o usuário no banco de dados
    usuario = await db.get(UsuarioModel, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    # Evita a atualização do ID
    usuario_update_data = usuario_update.model_dump(exclude_unset=True)

    # Se o usuário tentar alterar a senha, devemos aplicar hashing novamente
    if "senha_hash" in usuario_update_data:
        usuario_update_data["senha_hash"] = bcrypt_context.hash(usuario_update_data["senha_hash"])

    # Atualiza os campos permitidos do usuário
    for key, value in usuario_update_data.items():
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
