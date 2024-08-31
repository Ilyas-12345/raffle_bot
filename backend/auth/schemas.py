from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    last_name: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    name: str
    last_name: str
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

