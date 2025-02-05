from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    grupo_politica_id = Column(Integer, ForeignKey('grupo_politica.id'))
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())

    grupo_politica = relationship("GrupoPolitica", back_populates="usuarios")
    emprestimos = relationship("Emprestimo", back_populates="usuario")