"""Nova coluna 'usuario_vinculo' para a tabela 'tb_usuarios' criada!

Revision ID: 08142ec3c812
Revises: c95ba554f212
Create Date: 2024-12-09 10:33:23.756937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08142ec3c812'
down_revision: Union[str, None] = 'c95ba554f212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_usuarios', sa.Column('usuario_vinculo', sa.String(length=100)))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_usuarios', 'usuario_vinculo')
    # ### end Alembic commands ###
