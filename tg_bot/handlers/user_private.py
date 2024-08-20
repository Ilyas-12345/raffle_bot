import random
import string

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, LinkPreviewOptions, ReplyKeyboardRemove
from aiogram import F

from config import URL_RAFFLE_CONDITION, URL_RAFFLE_PERSONAL_DATA_PROCESSING
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


@user_private_router.message(StateFilter(None), CommandStart())
async def go_to_start_register_raffle(message: Message, state: FSMContext):
    await message.answer('Перед началом регистрации вам необдходимо ответить на вопросы\n',
                         reply_markup=get_reply_keyboard(
                             'Готов!',
                             'Не сейчас!',
                             size=(1,1,)
                         ))
    await state.set_state(QuestionBeforeRegister.first_Q)

#----Первый вопрос
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


@user_private_router.message(QuestionBeforeRegister.first_Q, F.text.casefold() == 'не сейчас!')
async def first_step_before_register_not_now(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Будем ждать в следующий раз!' )


@user_private_router.message(QuestionBeforeRegister.first_Q)
async def first_step_before_register_incorrect(message: Message, state: FSMContext):
    await message.answer('Я вас не понял(\n'
                         'Выберите \'Готов\' или \'Не сейчас!\'',
                         reply_markup=get_reply_keyboard(
                             'Готов!',
                             'Не сейчас!',
                             size=(1, 1,)
                         ))

#----Второй вопрос
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

@user_private_router.message(QuestionBeforeRegister.second_Q, F.text.casefold() == 'нет')
async def second_step_before_register_not_now(message: Message, state: FSMContext):
    await state.clear()
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

#Переход ко 2ой FSM
@user_private_router.message(RegistrationUser.contact, F.text.casefold() == 'да')
async def first_step_register(message: Message, state: FSMContext):
    await message.answer('Отлично!\n\n'
                         'Давайте приступим к регистрации.\n'
                         '1. Введите номер телефона в формате: 375 XX YYY-YY-YY или 8 0XX YYY-YY-YY',
                         reply_markup=get_reply_keyboard('Отправить номер телефона'))
    await state.set_state(RegistrationUser.name)


@user_private_router.message(RegistrationUser.name, F.text)
async def second_step_register_number(message: Message, state: FSMContext):
    if check_phone_number(message):
        await state.set_state(RegistrationUser.last_name)
        await message.answer(f'Отлично! Ваш номер телефона - {message.text}')
        await message.answer('Введите ваше имя')

    else:
        await message.answer('Некорректный номер телефона\n'
                             'Введите номер телефона еще раз.')


@user_private_router.message(RegistrationUser.last_name, F.text)
async def third_step_register(message: Message, state: FSMContext):
    await message.answer('Введите вашу фамилию')
    await state.set_state(RegistrationUser.surname)


@user_private_router.message(RegistrationUser.surname, F.text)
async def fours_step_register(message: Message, state: FSMContext):
    await message.answer('Введите ваше отчество')
    await state.set_state(RegistrationUser.check_number)


@user_private_router.message(RegistrationUser.check_number, F.text)
async def sixs_step_register(message: Message, state: FSMContext):
    alphanumeric = string.ascii_letters + string.digits
    random_value = ''.join(random.choice(alphanumeric) for _ in range(8))
    await message.answer('Вы успешно зарегестрировались в розыгрыше!\n'
                         f'Ваш код участника - {random_value}\n\n'
                         f'Спасибо что приняли участие, <b>{message.from_user.full_name}</b>',
                         parse_mode=ParseMode.HTML)
    await state.clear()

