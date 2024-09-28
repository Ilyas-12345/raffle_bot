from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.backend import auth_backend
from backend.auth.user_db import User
from backend.auth.user_manager import get_user_manager
from backend.botSettings import schemas
from backend.botSettings.crud import set_bot_dates, \
    get_lifetime_dates, display_raffle_participants, participant_and_raffles, show_participant_by_raffle_id, \
    all_participant_from_all_time, all_winner_from_all_raffle, get_winners_table, update_setting_time_activity_raffle, \
    update_amount_winner
from tg_bot.db.engine import get_async_session

router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


async def superuser_required(user: User = Depends(fastapi_users.current_user(active=True))):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action.")


# For all user(Manager/Admin
@router.get('/participant_raffles', response_model=list[schemas.Participant])
async def reg_users_by_raffle_id(raffle_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        participant = await show_participant_by_raffle_id(raffle_id=raffle_id, session=session)
        return participant
    except Exception as e:
        raise e


# For only Admin
@router.post('/set_time_bot', dependencies=[Depends(superuser_required)])
async def create_raffle(time_dates_activity: schemas.TimeActivityBot,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        time_dates = await set_bot_dates(session=session, dates_data=time_dates_activity)
        return time_dates
    except Exception as e:
        raise e


@router.get('/get_time_bot')
async def get_raffle(session: AsyncSession = Depends(get_async_session)):
    life_time = await get_lifetime_dates(session=session)
    return life_time


@router.get('/participant_raffle_by_id')
async def get_participant(raffle_id: int, session: AsyncSession = Depends(get_async_session)):
    participant = await display_raffle_participants(raffle_id=raffle_id, session=session)
    return participant


@router.get('/search_participant_by_phone')
async def participant_by_phone(phone_number: str, session: AsyncSession = Depends(get_async_session)):
    try:
        participant = await participant_and_raffles(phone_number=phone_number, session=session)
        return participant
    except Exception as e:
        raise e


@router.get('/get_alL_participant', response_model=list[schemas.Participant])
async def get_all_participant(session: AsyncSession = Depends(get_async_session)):
    try:
        users = await all_participant_from_all_time(session=session)
        return users
    except Exception as e:
        raise e


@router.get('/get_winner_all_time')
async def get_winners_all_raffles(session: AsyncSession = Depends(get_async_session)):
    try:
        winners = await all_winner_from_all_raffle(session=session)
        return winners
    except Exception as e:
        raise e


@router.get('/get_winners_raffle_id')
async def get_winners_raffle_id(raffle_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        raffle_winners = await get_winners_table(raffle_id=raffle_id, session=session)
        return raffle_winners
    except Exception as e:
        raise e


@router.patch('/update_time_activity', dependencies=[Depends(superuser_required)])
async def update_date_raffle(raffle_id: int, time_start: datetime, time_end: datetime,
                             session: AsyncSession = Depends(get_async_session)):
    try:
        result = await update_setting_time_activity_raffle(raffle_id=raffle_id, new_time_end=time_end,
                                                           new_time_start=time_start, session=session)
        return result
    except Exception as e:
        raise e


@router.patch('/update_amount_winner_activity', dependencies=[Depends(superuser_required)])
async def update_amount_winner_raffle(raffle_id: int, amount: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await update_amount_winner(raffle_id=raffle_id, amount=amount, session=session)
        return result
    except Exception as e:
        raise e