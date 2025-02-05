from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



# Tabela de associação para o relacionamento muitos-para-muitos entre GrupoPolitica e Permissao
grupo_politica_permissao = Table(
    'grupo_politica_permissao',
    Base.metadata,
    Column('grupo_politica_id', Integer, ForeignKey('grupo_politica.id'), primary_key=True),
    Column('permissao_id', Integer, ForeignKey('permissao.id'), primary_key=True)
)