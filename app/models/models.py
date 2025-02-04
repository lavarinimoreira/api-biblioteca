# Tabelas
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(15))
    endereco_completo = Column(String(200))
    senha_hash = Column(String(255), nullable=False)
    grupo_politica = Column(String(50))
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    emprestimos = relationship("Emprestimo", back_populates="usuario")

class Livro(Base):
    __tablename__ = 'livro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50))
    editora = Column(String(100))
    ano_publicacao = Column(Integer)
    numero_paginas = Column(Integer)
    quantidade_disponivel = Column(Integer, nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    emprestimos = relationship("Emprestimo", back_populates="livro")

class Emprestimo(Base):
    __tablename__ = 'emprestimo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    livro_id = Column(Integer, ForeignKey('livro.id'), nullable=False)
    data_emprestimo = Column(DateTime, default=func.now())
    data_devolucao = Column(DateTime)
    numero_renovacoes = Column(Integer, default=0)
    status = Column(String(20), nullable=False)
    usuario = relationship("Usuario", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos")