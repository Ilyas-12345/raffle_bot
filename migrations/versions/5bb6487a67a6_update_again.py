"""Update again

Revision ID: 5bb6487a67a6
Revises: f3b234c78851
Create Date: 2024-09-26 14:00:00.496306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bb6487a67a6'
down_revision: Union[str, None] = 'f3b234c78851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('winner_table',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('raffle_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.ForeignKeyConstraint(['raffle_id'], ['time_activity_bot.id'], ),
    sa.PrimaryKeyConstraint('participant_id', 'raffle_id')
    )
    op.drop_table('winner_time_activity_bot')
    op.drop_table('participant_winner')
    op.drop_table('winner')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('winner',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('winner_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('raffle_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['raffle_id'], ['time_activity_bot.id'], name='winner_raffle_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='winner_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('participant_winner',
    sa.Column('participant_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('winner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], name='participant_winner_participant_id_fkey'),
    sa.ForeignKeyConstraint(['winner_id'], ['winner.id'], name='participant_winner_winner_id_fkey'),
    sa.PrimaryKeyConstraint('participant_id', 'winner_id', name='participant_winner_pkey')
    )
    op.create_table('winner_time_activity_bot',
    sa.Column('winner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('time_activity_bot_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['time_activity_bot_id'], ['time_activity_bot.id'], name='winner_time_activity_bot_time_activity_bot_id_fkey'),
    sa.ForeignKeyConstraint(['winner_id'], ['winner.id'], name='winner_time_activity_bot_winner_id_fkey'),
    sa.PrimaryKeyConstraint('winner_id', 'time_activity_bot_id', name='winner_time_activity_bot_pkey')
    )
    op.drop_table('winner_table')
    # ### end Alembic commands ###
