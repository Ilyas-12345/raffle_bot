from aiogram.types import Message


def check_phone_number(message: Message):

    phone_number = ''.join(filter(str.isdigit, message.text))

    if len(phone_number) == 12 and phone_number.startswith('375') and phone_number[3:5] in ['25', '29', '33', '44']:
        return True

    elif len(phone_number) == 11 and phone_number.startswith('80') and phone_number[2:4] in ['25', '29', '33', '44']:
        return True

    else:
        return False

