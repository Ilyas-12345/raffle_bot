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
