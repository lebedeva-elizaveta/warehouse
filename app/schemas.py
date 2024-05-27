from pydantic import BaseModel, Field
from typing import Optional
import datetime


class RollCreate(BaseModel):
    length: float = Field()
    weight: float = Field()


class RollResponse(RollCreate):
    id: int
    added_date: datetime.datetime
    removed_date: Optional[datetime.datetime]

    class Config:
        from_attributes = True
