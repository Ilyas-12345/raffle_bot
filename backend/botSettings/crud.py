from datetime import timezone, timedelta, datetime
import random
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from tg_bot.db.models import Participant, TimeActivityBot, participant_time_activity_bot, winner
from backend.botSettings import schemas


async def show_participant_by_raffle_id(raffle_id: int, session: AsyncSession):
    query = (select(Participant).join(participant_time_activity_bot).
             where(participant_time_activity_bot.c.time_activity_bot_id == raffle_id))

    if query is None:
        raise HTTPException(status_code=404, detail=f"Raffle with ID {raffle_id} not found.")

    result = await session.execute(query)
    users = result.scalars().all()
    return users


async def set_bot_dates(dates_data: schemas.TimeActivityBot, session: AsyncSession):
    time_start = dates_data.time_start.astimezone(timezone(timedelta(hours=3))).replace(tzinfo=None, microsecond=0)
    time_end = dates_data.time_end.astimezone(timezone(timedelta(hours=3))).replace(tzinfo=None, microsecond=0)

    query = select(TimeActivityBot).where(
        (TimeActivityBot.time_start <= time_end) &
        (TimeActivityBot.time_end >= time_start)
    )
    result = await session.execute(query)
    existing_dates = result.scalars().all()

    if existing_dates:
        raise HTTPException(status_code=409, detail="Указанное время для розыгрыша пересекается с уже существующим розыгрышем в базе данных.")

    set_dates = TimeActivityBot(time_start=time_start,
                                time_end=time_end,
                                amount_winner=dates_data.amount_winner)
    session.add(set_dates)
    await session.commit()
    await session.refresh(set_dates)
    return set_dates


async def get_current_raffle(session: AsyncSession) -> Optional[TimeActivityBot]:
    stmt = select(TimeActivityBot).options(selectinload(TimeActivityBot.participants)).filter(
        TimeActivityBot.time_start <= datetime.now(),
        TimeActivityBot.time_end >= datetime.now()
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_lifetime_dates(session: AsyncSession):
    get_lifetime = await session.execute(select(TimeActivityBot).order_by(desc(TimeActivityBot.id)).limit(1))
    last_lifetime = get_lifetime.scalars().first()
    return last_lifetime


async def get_raffle_by_id(raffle_id: int, session: AsyncSession):
    raffle_by_id = select(TimeActivityBot).options(selectinload(TimeActivityBot.participants)).filter(
        TimeActivityBot.id == raffle_id
    )
    if raffle_by_id is None:
        raise HTTPException(status_code=404, detail=f'Розыгрыш с id {raffle_id} не найден')
    result = await session.execute(raffle_by_id)
    return result.scalars().first()


async def get_last_active_raffle(session: AsyncSession):
    current_time = datetime.now()
    stmt = select(TimeActivityBot).where(TimeActivityBot.time_end <= current_time).order_by(
        TimeActivityBot.time_end.desc()).limit(1)
    result = await session.execute(stmt)
    return result.scalars().first()


async def display_raffle_participants(raffle_id: int, session: AsyncSession):
    try:
        raffle = await get_raffle_by_id(session=session, raffle_id=raffle_id)
        participants = raffle.participants
        return participants
    except Exception as e:
        raise e


async def get_participant_phone_number(phone_number: str, session: AsyncSession):
    participant = select(Participant).options(selectinload(Participant.time_activity_bots)).filter(
        Participant.phone_number == phone_number
    )
    result = await session.execute(participant)
    return result.scalars().all()


async def participant_and_raffles(phone_number: str, session: AsyncSession):
    users = await get_participant_phone_number(phone_number=phone_number, session=session)
    if not users:
        raise HTTPException(status_code=404, detail="Пользователь с таким телефонрм {phone_number} не найден.")

    raffle = []
    for user in users:
        raffles = user.time_activity_bots
        raffle.append(raffles)

    if not raffle:
        raise HTTPException(status_code=404, detail=f'Не найдено ни одной лотереи для пользователя с номером телефона {phone_number}')

    return raffle


async def get_raffle_participant(raffle_id: int, session: AsyncSession):
    query = select(Participant).join(participant_time_activity_bot).where(
        participant_time_activity_bot.c.time_activity_bot_id == raffle_id)
    result = await session.execute(query)
    participants = result.scalars().all()
    return participants


async def get_winners_table(raffle_id: int, session: AsyncSession):
    query = select(Participant).join(winner).where(winner.c.raffle_id == raffle_id)
    if query is None:
        raise HTTPException(status_code=404, detail=f'Победители розыгрыша с id {raffle_id} не найдены')
    result = await session.execute(query)
    winners = result.scalars().all()
    return winners


async def all_participant_from_all_time(session: AsyncSession):
    query = select(Participant)
    if query is None:
        raise HTTPException(status_code=404, detail='Пользователей нет')
    result = await session.execute(query)
    participants = result.scalars().all()
    return participants


async def all_winner_from_all_raffle(session: AsyncSession):
    query = select(Participant).join(winner)
    result = await session.execute(query)
    winners = result.scalars().all()
    if not winners:
        raise HTTPException(status_code=404, detail='Победителей еще нет')
    return winners


async def update_setting_time_activity_raffle(raffle_id: int, new_time_start: datetime,
                                              new_time_end: datetime, session: AsyncSession):
    query = (update(TimeActivityBot).where(TimeActivityBot.id == raffle_id).
             values(time_start=new_time_start, time_end=new_time_end))

    if TimeActivityBot.id is None:
        raise HTTPException(status_code=404, detail=f'Розыгрыш с данным id {raffle_id} не найден')
    else:
        await session.execute(query)
        await session.commit()


async def update_amount_winner(raffle_id: int, amount: id, session: AsyncSession):
    query = update(TimeActivityBot).where(TimeActivityBot.id == raffle_id).values(amount_winner=amount)
    if query is None:
        raise HTTPException(status_code=404, detail=f'Розыгрыш с данным id {raffle_id} не найден')
    else:
        await session.execute(query)
        await session.commit()