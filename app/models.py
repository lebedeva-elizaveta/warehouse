from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Roll(Base):
    __tablename__ = "rolls"

    id = Column(Integer, primary_key=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    added_date = Column(Date, default=datetime.datetime.now().date())
    removed_date = Column(Date, nullable=True, default=None)
