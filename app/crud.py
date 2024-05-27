import datetime
from typing import Dict, Union, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.filter import RollFilter
from app.models import Roll
from app.schemas import RollResponse
from app.statistics import RollStatistics


class RollCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_roll(self, schema: schemas.RollCreate) -> models.Roll:
        """Создает новый рулон на складе и возвращает его"""
        db_roll = models.Roll(**schema.dict())
        self.db.add(db_roll)
        self.db.commit()
        self.db.refresh(db_roll)
        return db_roll

    def delete_roll(self, roll_id: int) -> models.Roll | None:
        """Удаляет рулон по ID со склада и возвращает его, если найден"""
        db_roll = self.db.query(models.Roll). \
            filter(models.Roll.id == roll_id).first()
        if db_roll:
            db_roll.removed_date = datetime.date.today()
            self.db.commit()
            return db_roll
        return None

    def get_rolls(self, roll_filter: RollFilter) -> list[RollResponse]:
        """
        Фильтрация по диапазонам:
        - id
        - длины
        - веса
        - дате добавления
        - дате удаления
        """
        query = roll_filter.filter(self.db.query(Roll))
        return query.all()

    def get_roll_statistics(
            self,
            start_date: datetime.date,
            end_date: datetime.date
    ) -> Dict[str, Optional[Union[int, float, datetime.date]]]:
        """
        Возвращает статистику по рулонам за указанный период:
        - количество добавленных рулонов
        - количество удалённых рулонов
        - средняя длина и вес рулонов
        - максимальная и минимальная длина и вес рулонов
        - суммарный вес рулонов
        - максимальный и минимальный промежуток
        между добавлением и удалением рулона
        - день с минимальным и максимальным количеством рулонов
        - день с минимальным и максимальным суммарным весом рулонов
        """

        if not self._check_if_exist():
            raise HTTPException(status_code=404, detail="No rolls found")

        roll_statistics = RollStatistics(self.db)
        return roll_statistics.calculate_statistics(start_date, end_date)

    def _check_if_exist(self) -> bool:
        """Проверяет, существуют ли рулоны в базе данных."""
        if self.db.query(models.Roll).count() > 0:
            return True
        else:
            return False
