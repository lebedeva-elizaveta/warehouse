"""Initial migration

Revision ID: fca979002c49
Revises: 
Create Date: 2024-05-26 21:39:38.347180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fca979002c49'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rolls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('added_date', sa.DateTime(), nullable=True),
    sa.Column('removed_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rolls_id'), 'rolls', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rolls_id'), table_name='rolls')
    op.drop_table('rolls')
    # ### end Alembic commands ###
