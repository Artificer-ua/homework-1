"""Init

Revision ID: 5505cab413e7
Revises: 6bc086d313f3
Create Date: 2024-01-29 23:55:23.904017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5505cab413e7'
down_revision: Union[str, None] = '6bc086d313f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_todos_title', table_name='todos')
    op.drop_table('todos')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.create_index('ix_todos_title', 'todos', ['title'], unique=True)
    # ### end Alembic commands ###
