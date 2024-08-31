from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.botSettings import schemas
from backend.botSettings.crud import show_participant
from tg_bot.db.engine import get_async_session

router = APIRouter()


@router.get('/participant')
async def reg_users(session: AsyncSession = Depends(get_async_session)):
    participant = await show_participant(session=session)
    return participant
