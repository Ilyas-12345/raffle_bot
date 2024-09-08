from datetime import timezone, timedelta

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from tg_bot.db.models import Participant, BotStatus, TimeActivityBot
from backend.botSettings import schemas


async def show_participant(session: AsyncSession):
    query = select(Participant)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


async def update_bot_activation(session: AsyncSession, bot_status_data: schemas.BotStatus):
    result = await session.execute(select(BotStatus))
    bot_status = result.scalars().first()

    if bot_status is None:
        bot_status = BotStatus(status=bot_status_data.status,
                               time_change_activity=bot_status_data.time_change_activity.now())
        session.add(bot_status)
    else:
        bot_status.status = bot_status_data.status
        bot_status.time_change_activity = bot_status_data.time_change_activity.now()

    await session.commit()
    await session.refresh(bot_status)
    return bot_status


async def get_bot_status(session: AsyncSession):
    get_status = await session.execute(select(BotStatus))
    bot_status = get_status.scalars().first()
    return bot_status


async def set_bot_dates(dates_data: schemas.SetActivityBot, session: AsyncSession):
    time_start = dates_data.time_start.astimezone(timezone(timedelta(hours=3))).replace(tzinfo=None, microsecond=0)
    time_end = dates_data.time_end.astimezone(timezone(timedelta(hours=3))).replace(tzinfo=None, microsecond=0)

    set_dates = TimeActivityBot(time_start=time_start,
                                time_end=time_end)
    session.add(set_dates)
    await session.commit()
    await session.refresh(set_dates)
    return set_dates


async def get_lifetime_dates(session: AsyncSession):
    get_lifetime = await session.execute(select(TimeActivityBot).order_by(desc(TimeActivityBot.id)).limit(1))
    last_lifetime = get_lifetime.scalars().first()
    return last_lifetime
