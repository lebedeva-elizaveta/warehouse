from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
import datetime

from pydantic import Field

from app import models


class RollFilter(Filter):
    id__gte: Optional[int] = Field(None)
    id__lte: Optional[int] = Field(None)
    length__gte: Optional[float] = Field(None)
    length__lte: Optional[float] = Field(None)
    weight__gte: Optional[float] = Field(None)
    weight__lte: Optional[float] = Field(None)
    added_date__gte: Optional[datetime.date] = Field(None)
    added_date__lte: Optional[datetime.date] = Field(None)
    removed_date__gte: Optional[datetime.date] = Field(None)
    removed_date__lte: Optional[datetime.date] = Field(None)

    class Constants(Filter.Constants):
        model = models.Roll

    class Config:
        populate_by_name = True
