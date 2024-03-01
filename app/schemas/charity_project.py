from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Field, validator, Extra
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    @validator('description')
    def name_description_null(cls, value):
        if not value:
            raise ValueError('Коментарий не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_than_zero(cls, value):
        if value < 0:
            raise ValueError(
                'Нуждаемая сума на проект не должна быть меньше нуля!'
            )
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., )
    full_amount: int = Field(..., gt=0)


class CharityProjectDB(CharityProjectBase):
    id: int
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
