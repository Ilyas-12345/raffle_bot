from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard(
        *btns: str,
        request_contact: int = None,
        place_holder: str = None,
        size: tuple[int] = (1,),
):

    keyboard = ReplyKeyboardBuilder()

    for text in btns:
        if request_contact == 1:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*size).as_markup(resize_keyboard=True)

