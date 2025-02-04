from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Schema para criação de novos livros
class LivroCreate(BaseModel):
    titulo: str
    autor: str
    genero: Optional[str] = None
    editora: Optional[str] = None
    ano_publicacao: Optional[int] = None
    numero_paginas: Optional[int] = None
    quantidade_disponivel: int
    isbn: str


# Schema para leitura de livros
class LivroRead(BaseModel):
    id: int
    titulo: str
    autor: str
    genero: Optional[str] = None
    editora: Optional[str] = None
    ano_publicacao: Optional[int] = None
    numero_paginas: Optional[int] = None
    quantidade_disponivel: int
    isbn: str
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True
