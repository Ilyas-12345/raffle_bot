"""empty message

Revision ID: 1deb52ce4e06
Revises: 6cd96904bdae
Create Date: 2024-09-24 23:36:20.640083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1deb52ce4e06'
down_revision: Union[str, None] = '6cd96904bdae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('winner_participant_id_fkey', 'winner', type_='foreignkey')
    op.drop_column('winner', 'participant_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('winner', sa.Column('participant_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('winner_participant_id_fkey', 'winner', 'participant', ['participant_id'], ['id'])
    # ### end Alembic commands ###
