from pydantic import BaseModel


class UserIn(BaseModel):
    telegram_id: int
    name: str


class UserOut(BaseModel):
    id: int
    telegram_id: int
    name: str

    class Config():
        from_attributes = True


class KeywordsIn(BaseModel):
    text: str


class KeywordsOut(BaseModel):
    id: int
    text: str

    class Config():
        from_attributes = True


class JobsIn(BaseModel):
    title: str
    description: str
    source: str
    url: str


class JobsOut(BaseModel):
    id: int
    title: str
    source: str
    description: str
    url: str

    class Config():
        from_attributes = True