from pydantic import BaseModel
from datetime import datetime

from tg_bot.db import models


class Participant(BaseModel):

    id: int
    username: str
    name: str
    last_name: str
    surname: str
    phone_number: str
    check_number: str
    random_key: str
    tg_id: int


class TimeActivityBot(BaseModel):

    time_start: datetime
    time_end: datetime
    amount_winner: int
    status: str


class Winner(BaseModel):

    raffle_id: int


class Question(BaseModel):

    q_first: str
    q_second: str
    q_second_raffle_condition_url: str
    q_third: str
    q_third_url_privacy: str
    q_fourth_introduce: str
    q_fourth_phone_number: str
    q_fives_name: str
    q_sixth_lastname: str
    q_seventh_middle_name: str
    q_eighth_sales_receipt: str


class Answer(BaseModel):

    a_end_registration_message: str
    a_message_for_winners: str
    a_message_for_all_users:  str
    a_cancel_registration: str
    a_if_user_say_no_now: str
    a_if_bot_dont_understand: str
    a_incorrect_phone_number: str
    a_no_found_raffle: str
    a_error_raffle: str
