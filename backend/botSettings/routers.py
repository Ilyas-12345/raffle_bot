from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.botSettings import schemas
from backend.botSettings.crud import show_participant, update_bot_activation, get_bot_status, set_bot_dates, \
    get_lifetime_dates
from tg_bot.db.engine import get_async_session

router = APIRouter()


@router.get('/participant')
async def reg_users(session: AsyncSession = Depends(get_async_session)):
    participant = await show_participant(session=session)
    return participant


@router.post('/change_activity')
async def change_activity(bot_status_activity: schemas.BotStatus,
                          session: AsyncSession = Depends(get_async_session)):
    status = await update_bot_activation(session=session, bot_status_data=bot_status_activity)
    return status


@router.get('/get_activity')
async def show_activity(session: AsyncSession = Depends(get_async_session)):
    result = await get_bot_status(session=session)
    return result


@router.post('/set_time_bot')
async def set_time(time_dates_activity: schemas.SetActivityBot,
                   session: AsyncSession = Depends(get_async_session)):
    time_dates = await set_bot_dates(session=session, dates_data=time_dates_activity)
    return time_dates


@router.get('/get_time_bot')
async def get_lifetime(session: AsyncSession = Depends(get_async_session)):
    life_time = await get_lifetime_dates(session=session)
    return life_time

