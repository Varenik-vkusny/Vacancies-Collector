from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class KeywordsIn(BaseModel):
    telegram_id: int
    text: str


class KeywordsOut(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)


class UserIn(BaseModel):
    telegram_id: int
    name: str


class UserOut(BaseModel):
    id: int
    telegram_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserWithKeywords(UserOut):
    keywords: List[KeywordsOut]

    model_config = ConfigDict(from_attributes=True)