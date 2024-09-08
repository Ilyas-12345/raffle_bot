from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


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


class BotStatus(Base):

    __tablename__ = 'bot_status'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[bool] = mapped_column(nullable=False)
    time_change_activity: Mapped[datetime] = mapped_column(nullable=False)


class TimeActivityBot(Base):

    __tablename__ = 'time_activity_bot'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_start: Mapped[datetime] = mapped_column(nullable=False)
    time_end: Mapped[datetime] = mapped_column(nullable=False)