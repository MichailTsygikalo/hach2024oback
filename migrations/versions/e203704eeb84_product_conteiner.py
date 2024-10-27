"""product - conteiner

Revision ID: e203704eeb84
Revises: aa993adb56d7
Create Date: 2024-10-27 00:10:36.138763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e203704eeb84'
down_revision: Union[str, None] = 'aa993adb56d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('container_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product', 'container', ['container_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'container_id')
    # ### end Alembic commands ###
