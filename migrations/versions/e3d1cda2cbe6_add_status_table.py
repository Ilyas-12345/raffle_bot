"""Add Status table

Revision ID: e3d1cda2cbe6
Revises: 01b0f196c8a1
Create Date: 2024-09-07 14:40:59.387151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3d1cda2cbe6'
down_revision: Union[str, None] = '01b0f196c8a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bot_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('time_change_activity', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bot_status')
    # ### end Alembic commands ###
