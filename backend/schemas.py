from pydantic import BaseModel


class UserIn(BaseModel):
    telegram_id: int
    name: str


class UserOut(BaseModel):
    id: int
    name: str
    keywords: str

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
    url: str


class JobsOut(BaseModel):
    id: int
    title: str
    description: str

    class Config():
        from_attributes = True