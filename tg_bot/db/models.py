from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey, Enum, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData()


participant_time_activity_bot = Table(
    'participant_time_activity_bot',
    Base.metadata,
    Column('participant_id', Integer, ForeignKey('participant.id'), primary_key=True),
    Column('time_activity_bot_id', Integer, ForeignKey('time_activity_bot.id'), primary_key=True)
)


winner = Table(
    'winner_table',
    Base.metadata,
    Column('participant_id', Integer, ForeignKey('participant.id'), primary_key=True),
    Column('raffle_id', Integer, ForeignKey('time_activity_bot.id'), primary_key=True)
)


class Participant(Base):
    __tablename__ = 'participant'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    check_number: Mapped[str] = mapped_column(nullable=False)
    random_key: Mapped[str] = mapped_column(nullable=False)
    tg_id: Mapped[int] = mapped_column(nullable=False)

    time_activity_bots: Mapped[list['TimeActivityBot']] = relationship(
        'TimeActivityBot',
        secondary=participant_time_activity_bot,
        back_populates='participants',
        lazy='selectin'
    )

    winners_raffle: Mapped[list['TimeActivityBot']] = relationship(
        'TimeActivityBot',
        secondary=winner,
        back_populates='winners',
        lazy='selectin'
    )


class TimeActivityBot(Base):
    __tablename__ = 'time_activity_bot'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_start: Mapped[datetime] = mapped_column(nullable=False)
    time_end: Mapped[datetime] = mapped_column(nullable=False)
    amount_winner: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(Enum('active', 'completed', name='raffle_status'), nullable=False, default='active')

    participants: Mapped[list['Participant']] = relationship(
        'Participant',
        secondary=participant_time_activity_bot,
        back_populates='time_activity_bots',
        lazy='selectin'
    )

    winners: Mapped[list['Participant']] = relationship(
        'Participant',
        secondary=winner,
        back_populates='winners_raffle',
        lazy='selectin'
    )


class QStepRegistration(Base):
    __tablename__ = 'question'

    #q - question
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    q_first: Mapped[str] = mapped_column(nullable=False)
    q_second: Mapped[str] = mapped_column(nullable=False)
    q_second_raffle_condition_url: Mapped[str] = mapped_column(nullable=False)
    q_third: Mapped[str] = mapped_column(nullable=False)
    q_third_url_privacy: Mapped[str] = mapped_column(nullable=False)
    q_fourth_introduce: Mapped[str] = mapped_column(nullable=False)
    q_fourth_phone_number: Mapped[str] = mapped_column(nullable=False)
    q_fives_name: Mapped[str] = mapped_column(nullable=False)
    q_sixth_lastname: Mapped[str] = mapped_column(nullable=False)
    q_seventh_middle_name: Mapped[str] = mapped_column(nullable=False)
    q_eighth_sales_receipt: Mapped[str] = mapped_column(nullable=False)


class ARegistration(Base):
    __tablename__ = 'answer'

    #a - answer
    id: Mapped[int] = mapped_column(primary_key=True)

    a_end_registration_message: Mapped[str] = mapped_column(nullable=False)
    a_message_for_winners: Mapped[str] = mapped_column(nullable=False)
    a_message_for_all_users: Mapped[str] = mapped_column(nullable=False)
    a_cancel_registration: Mapped[str] = mapped_column(nullable=False)
    a_if_user_say_no_now: Mapped[str] = mapped_column(nullable=False)
    a_if_bot_dont_understand: Mapped[str] = mapped_column(nullable=False)
    a_incorrect_phone_number: Mapped[str] = mapped_column(nullable=False)
    a_no_found_raffle: Mapped[str] = mapped_column(nullable=False)
    a_error_raffle: Mapped[str] = mapped_column(nullable=False)


