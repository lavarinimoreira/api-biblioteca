"""Atualizacao GrupoPolitica e Permissao

Revision ID: 5c1facd7a0cb
Revises: 857ee0b93369
Create Date: 2025-02-04 14:02:39.552045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c1facd7a0cb'
down_revision: Union[str, None] = '857ee0b93369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grupo_politica',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_atualizacao', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('permissao',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.Column('namespace', sa.String(length=100), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_atualizacao', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('grupo_politica_permissao',
    sa.Column('grupo_politica_id', sa.Integer(), nullable=False),
    sa.Column('permissao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grupo_politica_id'], ['grupo_politica.id'], ),
    sa.ForeignKeyConstraint(['permissao_id'], ['permissao.id'], ),
    sa.PrimaryKeyConstraint('grupo_politica_id', 'permissao_id')
    )
    op.add_column('usuario', sa.Column('grupo_politica_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'usuario', 'grupo_politica', ['grupo_politica_id'], ['id'])
    op.drop_column('usuario', 'grupo_politica')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('grupo_politica', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_column('usuario', 'grupo_politica_id')
    op.drop_table('grupo_politica_permissao')
    op.drop_table('permissao')
    op.drop_table('grupo_politica')
    # ### end Alembic commands ###
