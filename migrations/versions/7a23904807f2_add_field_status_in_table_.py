"""Add field /status/ in table TimeBotActivity

Revision ID: 7a23904807f2
Revises: 6c6dc1c2349f
Create Date: 2024-09-24 20:53:36.220259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a23904807f2'
down_revision: Union[str, None] = '6c6dc1c2349f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE raffle_status AS ENUM ('active', 'completed');")
    op.add_column('time_activity_bot', sa.Column('status', sa.Enum('active', 'completed', name='raffle_status'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('time_activity_bot', 'status')
    # ### end Alembic commands ###
