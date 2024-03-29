"""Release_13

Revision ID: 9105bc338a04
Revises: 15840ab347fd
Create Date: 2024-02-01 23:40:33.993741

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9105bc338a04"
down_revision: Union[str, None] = "15840ab347fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("confirmed", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "confirmed")
    # ### end Alembic commands ###
