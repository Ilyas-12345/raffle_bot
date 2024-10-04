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
    update_amount_winner, create_questions_table, update_all_question, update_q_first, update_q_second, \
    update_q_second_raffle_condition_url, update_q_third, update_q_third_url_privacy, update_q_fourth_introduce, \
    update_q_fourth_phone_number, update_q_fives_name, update_q_sixth_lastname, update_q_seventh_middle_name, \
    update_q_eighth_sales_receipt
from tg_bot.db.engine import get_async_session

router_admin = APIRouter()
router_all_user = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


async def superuser_required(user: User = Depends(fastapi_users.current_user(active=True))):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action.")


# For all user(Manager/Admin
@router_all_user.get('/participant_raffles', response_model=list[schemas.Participant])
async def reg_users_by_raffle_id(raffle_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        participant = await show_participant_by_raffle_id(raffle_id=raffle_id, session=session)
        return participant
    except Exception as e:
        raise e


# For only Admin
@router_admin.post('/set_time_bot', dependencies=[Depends(superuser_required)])
async def create_raffle(time_dates_activity: schemas.TimeActivityBot,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        time_dates = await set_bot_dates(session=session, dates_data=time_dates_activity)
        return time_dates
    except Exception as e:
        raise e


@router_all_user.get('/get_time_bot')
async def get_raffle(session: AsyncSession = Depends(get_async_session)):
    life_time = await get_lifetime_dates(session=session)
    return life_time


@router_all_user.get('/participant_raffle_by_id')
async def get_participant(raffle_id: int, session: AsyncSession = Depends(get_async_session)):
    participant = await display_raffle_participants(raffle_id=raffle_id, session=session)
    return participant


@router_all_user.get('/search_participant_by_phone')
async def participant_by_phone(phone_number: str, session: AsyncSession = Depends(get_async_session)):
    try:
        participant = await participant_and_raffles(phone_number=phone_number, session=session)
        return participant
    except Exception as e:
        raise e


@router_all_user.get('/get_alL_participant', response_model=list[schemas.Participant])
async def get_all_participant(session: AsyncSession = Depends(get_async_session)):
    try:
        users = await all_participant_from_all_time(session=session)
        return users
    except Exception as e:
        raise e


@router_all_user.get('/get_winner_all_time')
async def get_winners_all_raffles(session: AsyncSession = Depends(get_async_session)):
    try:
        winners = await all_winner_from_all_raffle(session=session)
        return winners
    except Exception as e:
        raise e


@router_all_user.get('/get_winners_raffle_id')
async def get_winners_raffle_id(raffle_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        raffle_winners = await get_winners_table(raffle_id=raffle_id, session=session)
        return raffle_winners
    except Exception as e:
        raise e


@router_admin.patch('/update_time_activity', dependencies=[Depends(superuser_required)])
async def update_date_raffle(raffle_id: int, time_start: datetime, time_end: datetime,
                             session: AsyncSession = Depends(get_async_session)):
    try:
        result = await update_setting_time_activity_raffle(raffle_id=raffle_id, new_time_end=time_end,
                                                           new_time_start=time_start, session=session)
        return result
    except Exception as e:
        raise e


@router_admin.patch('/update_amount_winner_activity', dependencies=[Depends(superuser_required)])
async def update_amount_winner_raffle(raffle_id: int, amount: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await update_amount_winner(raffle_id=raffle_id, amount=amount, session=session)
        return result
    except Exception as e:
        raise e


@router_all_user.post('/create_question')
async def creat_question(questions_data: schemas.Question, session: AsyncSession = Depends(get_async_session)):
    questions = await create_questions_table(question=questions_data, session=session)
    return questions


@router_all_user.put('/update_alL_question')
async def update_question_table(questions_data: schemas.Question, session: AsyncSession = Depends(get_async_session)):
    questions = await update_all_question(new_data=questions_data, session=session)
    return questions


@router_all_user.patch('/update_q1')
async def update_q1(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_first(question=question, session=session)
    return question


@router_all_user.patch('/update_q2')
async def update_q2(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_second(question=question, session=session)
    return question


@router_all_user.patch('/update_q2.2')
async def update_q2_raffle_url(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_second_raffle_condition_url(question=question, session=session)
    return question


@router_all_user.patch('/update_q3')
async def update_q3(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_third(question=question, session=session)
    return question


@router_all_user.patch('/update_q3.1')
async def update_q3_url_privacy(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_third_url_privacy(question=question, session=session)
    return question


@router_all_user.patch('/update_q4')
async def update_q4_introduce(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_fourth_introduce(question=question, session=session)
    return question


@router_all_user.patch('/update_q4.1')
async def update_q4_phone_number(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_fourth_phone_number(question=question, session=session)
    return question


@router_all_user.patch('/update_q5')
async def update_q5_name(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_fives_name(question=question, session=session)
    return question


@router_all_user.patch('/update_q6')
async def update_q6_lastname(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_sixth_lastname    (question=question, session=session)
    return question


@router_all_user.patch('/update_q7')
async def update_q7_middle_name(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_seventh_middle_name(question=question, session=session)
    return question


@router_all_user.patch('/update_q8')
async def update_q8_sales_receipt(question: str, session: AsyncSession = Depends(get_async_session)):
    question = await update_q_eighth_sales_receipt(question=question, session=session)
    return question


