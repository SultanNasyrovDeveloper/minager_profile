from typing import Optional

from pydantic import BaseModel


class UserProfileSchema(BaseModel):
    user_id: str
    last_name: str
    first_name: str
    patronymic: str


class UserProfileEditSchema(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
