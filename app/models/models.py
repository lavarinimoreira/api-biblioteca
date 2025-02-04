# Tabelas
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



# Tabela de associação para o relacionamento muitos-para-muitos entre GrupoPolitica e Permissao
grupo_politica_permissao = Table(
    'grupo_politica_permissao',
    Base.metadata,
    Column('grupo_politica_id', Integer, ForeignKey('grupo_politica.id'), primary_key=True),
    Column('permissao_id', Integer, ForeignKey('permissao.id'), primary_key=True)
)


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(15))
    endereco_completo = Column(String(200))
    senha_hash = Column(String(255), nullable=False)
    grupo_politica_id = Column(Integer, ForeignKey('grupo_politica.id'))
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())

    grupo_politica = relationship("GrupoPolitica", back_populates="usuarios")
    emprestimos = relationship("Emprestimo", back_populates="usuario")


class GrupoPolitica(Base):
    __tablename__ = 'grupo_politica'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())

    usuarios = relationship("Usuario", back_populates="grupo_politica")
    permissoes = relationship("Permissao", secondary=grupo_politica_permissao, back_populates="grupos_politica")

class Permissao(Base):
    __tablename__ = 'permissao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255))
    namespace = Column(String(100))
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())

    grupos_politica = relationship("GrupoPolitica", secondary=grupo_politica_permissao, back_populates="permissoes")


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