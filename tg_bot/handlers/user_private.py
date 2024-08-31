import random
import string

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, LinkPreviewOptions, ReplyKeyboardRemove
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

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
    await message.answer('Перед началом регистрации вам необдходимо ответить на вопросы\n',
                         reply_markup=get_reply_keyboard(
                             'Готов!',
                             'Не сейчас!',
                             size=(1,1,)
                         ))
    await session.begin()
    await state.set_state(QuestionBeforeRegister.first_Q)


@user_private_router.message(Command(commands=["cancel"]))
@user_private_router.message(F.text.casefold() == 'отмена')
async def go_to_start_register_raffle(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await session.rollback()
    await message.answer('Регистрация отменена',
                         reply_markup=ReplyKeyboardRemove())


@user_private_router.message(QuestionBeforeRegister.first_Q, F.text.casefold() == 'готов!')
async def first_step_before_register(message: Message, state: FSMContext):
    link = URL_RAFFLE_CONDITION
    await message.answer(f"Вы ознакомились с условиями розыгрышами?"
                         f"Ознакомиться можно здесь -> {link}",
                         link_preview_options=LinkPreviewOptions(is_disabled=True),
                         reply_markup=get_reply_keyboard(
                             'Да',
                             'Нет',
                             size=(1,1,)
                         ))
    await state.set_state(QuestionBeforeRegister.second_Q)
#----Первый вопрос


@user_private_router.message(QuestionBeforeRegister.first_Q, F.text.casefold() == 'не сейчас!')
async def first_step_before_register_not_now(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await session.rollback()
    await message.answer('Будем ждать в следующий раз!',
                         reply_markup=ReplyKeyboardRemove())


@user_private_router.message(QuestionBeforeRegister.first_Q)
async def first_step_before_register_incorrect(message: Message, state: FSMContext):
    await message.answer('Я вас не понял(\n'
                         'Выберите \'Готов\' или \'Не сейчас!\'',
                         reply_markup=get_reply_keyboard(
                             'Готов!',
                             'Не сейчас!',
                             size=(1, 1,)
                         ))

@user_private_router.message(QuestionBeforeRegister.second_Q, F.text.casefold() == 'да')
async def second_step_before_register(message: Message, state: FSMContext):
    link = URL_RAFFLE_PERSONAL_DATA_PROCESSING
    await message.answer(f'Вы даете подтверждение на обработку персональных данных?'
                         f'Ссылка для ознакомления -> {link}: ',
                         reply_markup=get_reply_keyboard(
                             'Да',
                             'Нет',
                             size=(1,1,)
                         ))
    await state.set_state(RegistrationUser.contact)
#----Второй вопрос

@user_private_router.message(QuestionBeforeRegister.second_Q, F.text.casefold() == 'нет')
async def second_step_before_register_not_now(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await session.rollback()
    await message.answer('Будем ждать в следующий раз!',
                         reply_markup=get_reply_keyboard(
                             '/start',
                             size=(1, 1,)
                         ))


@user_private_router.message(QuestionBeforeRegister.second_Q)
async def second_step_before_register_incorrect(message: Message):
    await message.answer('Я вас не понял(\n'
                         'Выберите \'Да\' или \'Нет\'',
                         reply_markup=get_reply_keyboard(
                             'Да',
                             'Нет',
                             size=(1, 1,)
                         ))

@user_private_router.message(RegistrationUser.contact, F.text.casefold() == 'да')
async def first_step_register(message: Message, state: FSMContext):
    await message.answer('Отлично!\n\n'
                         'Давайте приступим к регистрации.\n'
                         '1. Введите номер телефона в формате: 375 XX YYY-YY-YY или 8 0XX YYY-YY-YY',
                         reply_markup=get_reply_keyboard('Отправить номер телефона'))
    await state.set_state(RegistrationUser.name)

#Переход ко 2ой FSM
@user_private_router.message(RegistrationUser.name, F.text)
async def second_step_register_number(message: Message, state: FSMContext):
    if check_phone_number(message):
        await state.update_data(contact=message.text)
        await state.set_state(RegistrationUser.last_name)
        await message.answer(f'Отлично! Ваш номер телефона - {message.text}')
        await message.answer('Введите ваше имя')

    else:
        await message.answer('Некорректный номер телефона\n'
                             'Введите номер телефона еще раз.')


@user_private_router.message(RegistrationUser.last_name, F.text)
async def third_step_register(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите вашу фамилию')
    await state.set_state(RegistrationUser.surname)


@user_private_router.message(RegistrationUser.surname, F.text)
async def fours_step_register(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('Введите ваше отчество')
    await state.set_state(RegistrationUser.check_number)


@user_private_router.message(RegistrationUser.check_number, F.text)
async def sixs_step_register(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer('Введите номер чека')
    await state.set_state(RegistrationUser.random_value)


@user_private_router.message(RegistrationUser.random_value, F.text)
async def sevens_step_register(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(check_number=message.text)
    alphanumeric = string.ascii_letters + string.digits
    random_value = ''.join(random.choice(alphanumeric) for _ in range(8))
    data = await state.get_data()
    user_data = {
        'username': message.from_user.full_name,
        'name': data.get('name'),
        'last_name': data.get('last_name'),
        'surname': data.get('surname'),
        'phone_number': data.get('contact'),
        'check_number': data.get('check_number'),
        'random_key': random_value
    }

    try:
        new_user = Participant(**user_data)
        session.add(new_user)
        await session.commit()
        await message.answer('Вы успешно зарегестрировались в розыгрыше!\n'
                             f'Ваш код участника - {random_value}\n\n'
                             f'Спасибо что приняли участие, <b>{message.from_user.full_name}</b>',
                             parse_mode=ParseMode.HTML)
        await state.clear()

    except Exception as e:
        await session.rollback()
        await message.answer('Произошла ошибка. Пройдите регистрацию заново')
        raise e

    finally:
        await session.close()

