from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import string
import random
import shutil

from app.models.user import Usuario as UsuarioModel
from app.models.book import Livro as LivroModel
from app.schemas.book import LivroOut
from app.schemas.user import UsuarioOut
from app.database import get_db
from app.services.security import get_current_user

router = APIRouter(prefix="/uploads", tags=["Uploads"])

# Adicionar imagem de perfil
@router.post("/profile", response_model=UsuarioOut, status_code=status.HTTP_200_OK)
async def upload_profile_picture(
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Busca o usuário no banco de dados com base no ID contido no dicionário
    stmt = select(UsuarioModel).where(UsuarioModel.id == current_user["id"])
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.profile_picture_url:
        old_file_path = Path(user.profile_picture_url)
        if old_file_path.exists():
            try:
                old_file_path.unlink()
            except Exception as e:
                raise HTTPException(status_code=500, detail="Erro ao remover imagem antiga")
    
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for _ in range(6))
    novo_nome = f"_{rand_str}."
    filename = novo_nome.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"
    
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    user.profile_picture_url = path
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user

# Adicionar imagem da capa do livro
@router.post("/book_cover", response_model=LivroOut, status_code=status.HTTP_200_OK)
async def upload_book_cover_image(
    book_id: int,
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verifica se o livro existe
    stmt = select(LivroModel).where(LivroModel.id == book_id)
    result = await db.execute(stmt)
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    
    # Verifica se o usuário atual tem permissão para atualizar o livro
    if "book.create" not in current_user.get("permissoes", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada.")
    
    # Se o livro já possui uma imagem, tenta removê-la para evitar arquivos órfãos
    if book.image_url:
        old_file_path = Path(book.image_url)
        if old_file_path.exists():
            try:
                old_file_path.unlink()  # Remove o arquivo antigo
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao remover a capa antiga")
    
    # Gera um nome único para o novo arquivo
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for _ in range(6))
    novo_nome = f"_{rand_str}."
    filename = novo_nome.join(image.filename.rsplit(".", 1))
    
    # Define o path para salvar a imagem
    path = f"images/{filename}"
    
    # Salva o arquivo no sistema de arquivos
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Atualiza o campo da capa do livro no banco de dados
    book.image_url = path
    db.add(book)
    await db.commit()
    await db.refresh(book)
    
    return book