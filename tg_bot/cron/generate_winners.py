import random
from datetime import datetime

import asyncio
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from backend.botSettings.crud import get_last_active_raffle, get_current_raffle, get_raffle_participant, \
    get_winners_table, get_answer_table
from tg_bot.db.models import winner, TimeActivityBot


async def determine_winners(raffle: TimeActivityBot, session: AsyncSession):
    if not raffle:
        raise ValueError(f"Raffle with ID {raffle.id} not found.")

    participants = await get_raffle_participant(raffle.id, session)
    if not participants:
        return (f"No participants found for raffle with ID {raffle.id}.")

    winners = random.sample(participants,  raffle.amount_winner)

    for user in winners:
        await session.execute(winner.insert().values(participant_id=user.id, raffle_id=raffle.id))

    await session.commit()


async def notify_winners(bot, winners, session: AsyncSession):
    answer = await get_answer_table(session=session)
    for Win in winners:
        message = f"{answer.a_message_for_winners}!"
        await bot.send_message(Win.tg_id, message)


async def monitor_raffles(bot: Bot, session: AsyncSession):
    while True:
        raffles = await get_last_active_raffle(session=session)

        if raffles is not None:
            if raffles.status != 'completed':
                answer = await get_answer_table(session=session)
                await determine_winners(session=session, raffle=raffles)
                winners = await get_winners_table(raffle_id=raffles.id, session=session)
                await notify_winners(bot, winners, session=session)

                raffles.status = 'completed'
                session.add(raffles)

                for user in raffles.participants:
                    winners_text = "\n".join([f"- {user.username}" for user in winners])
                    await bot.send_message(chat_id=user.tg_id,
                                           text=f"{answer.a_message_for_all_users}\n "
                                                f"{winners_text}")

        await session.commit()
        await asyncio.sleep(60)
