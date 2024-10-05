import random
import string
from datetime import datetime

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, LinkPreviewOptions, ReplyKeyboardRemove
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

from backend.botSettings.crud import get_lifetime_dates, get_current_raffle, get_question_table, get_answer_table
from config import URL_RAFFLE_CONDITION, URL_RAFFLE_PERSONAL_DATA_PROCESSING
from tg_bot.db.models import Participant
from tg_bot.keyboard.reply_keyboard import get_reply_keyboard
from tg_bot.validation.phone_number import check_phone_number

user_private_router = Router()


class QuestionBeforeRegister(StatesGroup):
    first_Q = State()
    second_Q = State()


class RegistrationUser(StatesGroup):
    contact = State()
    name = State()
    last_name = State()
    surname = State()
    check_number = State()
    random_value = State()


@user_private_router.message(StateFilter(None), CommandStart())
async def go_to_start_register_raffle(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await message.answer(f'{questions.q_first}\n',
                         reply_markup=get_reply_keyboard(
                             'Начать!',
                            'Не сейчас!',
                            'Отмена',
                             size=(2, 1)
                         ))
    await state.set_state(QuestionBeforeRegister.first_Q)


@user_private_router.message(F.text.casefold().in_(["отмена", "/cancel"]))
async def go_to_start_register_raffle(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await session.rollback()
    answer = await get_answer_table(session=session)
    await message.answer(f'{answer.a_cancel_registration}',
                         reply_markup=get_reply_keyboard(
                             'Начать!',
                             'Не сейчас!',
                             'Отмена',
                             size=(2, 1)
                         ))


@user_private_router.message(F.text.casefold() == 'начать!')
async def first_step_before_register(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await message.answer(f"{questions.q_second}\n{questions.q_second_raffle_condition_url}",
                         link_preview_options=LinkPreviewOptions(is_disabled=True),
                         reply_markup=get_reply_keyboard(
                             'Да',
                             'Нет',
                             'Отмена',
                             size=(2, 1)
                         ))
    await state.set_state(QuestionBeforeRegister.second_Q)


@user_private_router.message(F.text.casefold().in_(["не сейчас", "нет"]))
async def first_step_before_register_not_now(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await session.rollback()
    answer = await get_answer_table(session=session)
    await message.answer(f"{answer.a_if_user_say_no_now}",
                         reply_markup=ReplyKeyboardRemove())


#----Первый вопрос
@user_private_router.message(QuestionBeforeRegister.first_Q)
async def first_step_before_register_incorrect(message: Message, state: FSMContext, session: AsyncSession):
    answer = await get_answer_table(session=session)
    await message.answer(f'{answer.a_if_bot_dont_understand}',
                         reply_markup=get_reply_keyboard(
                             'Начать!',
                             'Не сейчас!',
                             'Отмена',
                             size=(2, 1)
                         ))


@user_private_router.message(QuestionBeforeRegister.second_Q, F.text.casefold() == 'да')
async def second_step_before_register(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await message.answer(f'{questions.q_third}\n{questions.q_third_url_privacy}: ',
                         reply_markup=get_reply_keyboard(
                             'Да',
                             'Нет',
                             'Отмена',
                             size=(2, 1)
                         ))
    await state.set_state(RegistrationUser.contact)


#----Второй вопрос
@user_private_router.message(QuestionBeforeRegister.second_Q, F.text.casefold() == 'нет')
async def second_step_before_register_not_now(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await session.rollback()
    answer = await get_answer_table(session=session)
    await message.answer(f'{answer.a_if_user_say_no_now}',
                         reply_markup=  get_reply_keyboard(
                             '/start',
                             size=(1, 1,)
                         ))

@user_private_router.message(QuestionBeforeRegister.second_Q)
async def second_step_before_register_incorrect(message: Message, session: AsyncSession):
    answer = await get_answer_table(session=session)
    await message.answer(f'{answer.a_if_bot_dont_understand}',
                         reply_markup=get_reply_keyboard(
                             'Да',
                             'Нет',
                             'Отмена',
                             size=(2, 1)
                         ))


@user_private_router.message(RegistrationUser.contact, F.text.casefold() == 'да')
async def first_step_register(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await message.answer(f'{questions.q_fourth_introduce}\n{questions.q_fourth_phone_number}',
                         reply_markup=get_reply_keyboard(
                             'Отмена',
                             size=(1,)))
    await state.set_state(RegistrationUser.name)


@user_private_router.message(RegistrationUser.name, F.text)
async def second_step_register_number(message: Message, state: FSMContext, session: AsyncSession):
    if check_phone_number(message):
        questions = await get_question_table(session=session)
        await state.update_data(contact=message.text)
        await state.set_state(RegistrationUser.last_name)
        await message.answer(f'{questions.q_fives_name}',
                             reply_markup=get_reply_keyboard(
                                 'Отмена',
                                 size=(1,)
                             ))

    else:
        answer = await get_answer_table(session=session)
        await message.answer(f'{answer.a_incorrect_phone_number}')


#Переход ко 2ой FSM
@user_private_router.message(RegistrationUser.last_name, F.text)
async def third_step_register(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await state.update_data(name=message.text)
    await message.answer(f'{questions.q_sixth_lastname}',
                         reply_markup=get_reply_keyboard(
                             'Отмена',
                             size=(1, )
                         ))
    await state.set_state(RegistrationUser.surname)


@user_private_router.message(RegistrationUser.surname, F.text)
async def fours_step_register(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await state.update_data(last_name=message.text)
    await message.answer(f'{questions.q_seventh_middle_name}',
                         reply_markup=get_reply_keyboard(
                             'Отмена',
                             size=(1, )
                         ))
    await state.set_state(RegistrationUser.check_number)


@user_private_router.message(RegistrationUser.check_number, F.text)
async def sixs_step_register(message: Message, state: FSMContext, session: AsyncSession):
    questions = await get_question_table(session=session)
    await state.update_data(surname=message.text)
    await message.answer(f'{questions.q_eighth_sales_receipt}',
                         reply_markup=get_reply_keyboard(
                             'Отмена',
                             size=(1, )
                         ))
    await state.set_state(RegistrationUser.random_value)


@user_private_router.message(RegistrationUser.random_value, F.text)
async def sevens_step_register(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(check_number=message.text)

    alphanumeric = string.ascii_letters + string.digits
    random_value = ''.join(random.choice(alphanumeric) for _ in range(8))

    answer = await get_answer_table(session=session)
    current_raffle = await get_current_raffle(session=session)
    if not current_raffle:
        await message.answer(f'{answer.a_no_found_raffle}')
        await state.clear()
        return

    data = await state.get_data()
    user_data = {
        'username': message.from_user.full_name,
        'name': data.get('name'),
        'last_name': data.get('last_name'),
        'surname': data.get('surname'),
        'phone_number': data.get('contact'),
        'check_number': data.get('check_number'),
        'random_key': random_value,
        'tg_id': message.from_user.id
    }

    try:
        new_user = Participant(**user_data)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        current_raffle.participants.append(new_user)
        await session.commit()
        await message.answer(f'{answer.a_end_registration_message}\n'
                             f'- {data.get('name')}'
                             f' {data.get('last_name')}'
                             f' {data.get('surname')}\n'
                             f'- {data.get('contact')}\n'
                             f'- {data.get('check_number')}\n'
                             f'- Код участника - {random_value}',
                             parse_mode=ParseMode.HTML)
        await state.clear()

    except Exception as e:
        await session.rollback()
        await message.answer(f'{answer.a_error_raffle}',
                             reply_markup=get_reply_keyboard(
                                 '/start',
                                 size=(1,)
                             ))
        await state.clear()
        raise e

    finally:
        await session.close()
