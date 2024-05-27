from datetime import date, timedelta
from typing import Dict, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


class RollStatistics:
    def __init__(self, db: Session):
        self.db = db

    def calculate_statistics(
            self,
            start_date: date,
            end_date: date
    ) -> Dict[str, Optional[Union[int, float, date]]]:
        statistics = self._initialize_statistics()
        self._basic_statistics(statistics, start_date, end_date)
        self._time_diff_statistics(statistics, start_date, end_date)
        self._day_statistics(statistics, start_date, end_date)
        return statistics

    @staticmethod
    def _initialize_statistics() -> \
            Dict[str, Optional[Union[int, float, date]]]:
        return {
            "total_added": 0,
            "total_removed": 0,
            "avg_length": 0.0,
            "avg_weight": 0.0,
            "max_length": 0.0,
            "min_length": 0.0,
            "max_weight": 0.0,
            "min_weight": 0.0,
            "total_weight": 0.0,
            "max_time_diff": 0,
            "min_time_diff": 0,
            "day_with_min_rolls_count": None,
            "day_with_max_rolls_count": None,
            "day_with_min_total_weight": None,
            "day_with_max_total_weight": None,
        }

    def _basic_statistics(
            self,
            statistics: Dict[str, Optional[Union[int, float, date]]],
            start_date: date,
            end_date: date
    ):
        statistics["total_added"] = \
            self.db.query(func.count(models.Roll.id)).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).scalar() or 0
        statistics["total_removed"] = \
            self.db.query(func.count(models.Roll.id)).filter(
            models.Roll.removed_date.between(start_date, end_date)
            ).scalar() or 0

        avg_length, avg_weight = self.db.query(
            func.avg(models.Roll.length), func.avg(models.Roll.weight)
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).first() or (0.0, 0.0)

        statistics["avg_length"] = avg_length
        statistics["avg_weight"] = avg_weight

        max_length, min_length = self.db.query(
            func.max(models.Roll.length), func.min(models.Roll.length)
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).first() or (0.0, 0.0)

        statistics["max_length"] = max_length
        statistics["min_length"] = min_length

        max_weight, min_weight = self.db.query(
            func.max(models.Roll.weight), func.min(models.Roll.weight)
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).first() or (0.0, 0.0)

        statistics["max_weight"] = max_weight
        statistics["min_weight"] = min_weight

        statistics["total_weight"] = self.db.query(
            func.sum(models.Roll.weight)
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).scalar() or 0.0

    def _time_diff_statistics(
            self,
            statistics: Dict[str, Optional[Union[int, float, date]]],
            start_date: date,
            end_date: date
    ):
        max_time_diff, min_time_diff = self.db.query(
            func.max(models.Roll.removed_date - models.Roll.added_date),
            func.min(models.Roll.removed_date - models.Roll.added_date)
        ).filter(
            models.Roll.removed_date.isnot(None),
            models.Roll.added_date.between(start_date, end_date),
            models.Roll.removed_date.between(start_date, end_date)
        ).first() or (timedelta(days=0), timedelta(days=0))

        statistics["max_time_diff"] = max_time_diff.days \
            if isinstance(max_time_diff, timedelta) else 0
        statistics["min_time_diff"] = min_time_diff.days \
            if isinstance(min_time_diff, timedelta) else 0

    def _day_statistics(
            self,
            statistics: Dict[str, Optional[Union[int, float, date]]],
            start_date: date,
            end_date: date
    ):
        day_with_min_rolls_count = self.db.query(
            models.Roll.added_date
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).group_by(
            models.Roll.added_date
        ).order_by(
            func.count(models.Roll.id)
        ).first()
        day_with_max_rolls_count = self.db.query(
            models.Roll.added_date
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).group_by(
            models.Roll.added_date
        ).order_by(
            func.count(models.Roll.id).desc()
        ).first()

        statistics["day_with_min_rolls_count"] = day_with_min_rolls_count[0] \
            if day_with_min_rolls_count else None
        statistics["day_with_max_rolls_count"] = day_with_max_rolls_count[0] \
            if day_with_max_rolls_count else None

        day_with_min_total_weight = self.db.query(
            models.Roll.added_date
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).group_by(
            models.Roll.added_date
        ).order_by(
            func.sum(models.Roll.weight)
        ).first()
        day_with_max_total_weight = self.db.query(
            models.Roll.added_date
        ).filter(
            models.Roll.added_date.between(start_date, end_date)
        ).group_by(
            models.Roll.added_date
        ).order_by(
            func.sum(models.Roll.weight).desc()
        ).first()

        statistics["day_with_min_total_weight"] = \
            day_with_min_total_weight[0] if day_with_min_total_weight else None
        statistics["day_with_max_total_weight"] = \
            day_with_max_total_weight[0] if day_with_max_total_weight else None
