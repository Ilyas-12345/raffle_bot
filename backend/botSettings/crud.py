from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tg_bot.db.models import Participant


async def show_participant(session: AsyncSession):
    query = select(Participant)
    result = await session.execute(query)
    users = result.scalars().all()
    return users
