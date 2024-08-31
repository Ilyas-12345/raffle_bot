from pydantic import BaseModel


class Participant(BaseModel):

    username: str
    name: str
    last_name: str
    surname: str
    phone_number: str
    check_number: str
    random_key: str
