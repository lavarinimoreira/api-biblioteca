from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base com campos comuns
class UsuarioBase(BaseModel):
    nome: str = Field(..., max_length=100)
    email: EmailStr
    telefone: Optional[str] = Field(None, max_length=15)
    endereco_completo: Optional[str] = Field(None, max_length=200)

# # Schema para criação (inclui senha)
class UsuarioCreate(UsuarioBase):
    senha_hash: str = Field(..., min_length=8, max_length=128)
    """
    O Pydantic v2 mudou a forma de definir exemplos nos schemas.
    Antes, você podia passar example diretamente no Field, 
    mas agora isso deve ser feito usando o parâmetro json_schema_extra:
    """
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Mussum",
                    "email": "mussum@gmail.com",
                    "telefone": "(31)99999-9999",
                    "endereco_completo": "Rua Piracicaba, número 567, Bairro Floresta.",
                    "senha_hash": "senhaSegura123"
                }
            ]
        }
    }


class UsuarioCreateAdmin(UsuarioCreate):
    grupo_politica: str = Field(..., max_length=32)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Novo Admin",
                    "email": "novo_admin@biblioteca.com",
                    "telefone": "(31)99999-9999",
                    "endereco_completo": "Rua Piracicaba, número 567, Bairro Floresta.",
                    "senha_hash": "senhaAdmin123",
                    "grupo_politica": "admin"
                }
            ]
        }
    }

# Schema para atualização (todos os campos opcionais)
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=15)
    endereco_completo: Optional[str] = Field(None, max_length=200)
    senha_hash: Optional[str] = Field(None, min_length=8, max_length=128)
    
class UsuarioAdminUpdate(UsuarioUpdate):
    grupo_politica: Optional[str] = None

# Schema para resposta (exclui a senha_hash)
class UsuarioOut(UsuarioBase):
    id: int
    data_criacao: datetime
    data_atualizacao: Optional[datetime]

    class Config:
        # orm_mode = True
        from_attributes = True
