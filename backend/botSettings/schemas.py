from pydantic import BaseModel
from datetime import datetime

class Participant(BaseModel):

    username: str
    name: str
    last_name: str
    surname: str
    phone_number: str
    check_number: str
    random_key: str


class BotStatus(BaseModel):

    status: bool
    time_change_activity: datetime


class SetActivityBot(BaseModel):

    time_start: datetime
    time_end: datetime
