from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from typing import List
import datetime

from app import schemas
from app.crud import RollCRUD
from app.deps import get_db
from app.filter import RollFilter

router = APIRouter()


@router.post("/rolls/", response_model=schemas.RollResponse)
async def create_roll(schema: schemas.RollCreate,
                      db: Session = Depends(get_db)):
    return RollCRUD(db).create_roll(schemas.RollCreate(**schema.dict()))


@router.delete("/rolls/{roll_id}/", response_model=schemas.RollResponse)
def delete_roll(roll_id: int, db: Session = Depends(get_db)):
    deleted_roll = RollCRUD(db).delete_roll(roll_id)
    if deleted_roll:
        return deleted_roll
    raise HTTPException(
        status_code=404,
        detail=f"Roll with id {roll_id} not found"
    )


@router.get("/rolls/", response_model=List[schemas.RollResponse])
def get_rolls(
        product_filter: RollFilter = FilterDepends(RollFilter),
        db: Session = Depends(get_db)
) -> list:
    rolls = RollCRUD(db).get_rolls(product_filter)
    if len(rolls) > 0:
        return rolls
    raise HTTPException(
        status_code=404,
        detail="Rolls not found"
    )


@router.get("/roll_statistics/")
def get_roll_statistics(
        start_date: datetime.date,
        end_date: datetime.date,
        db: Session = Depends(get_db)
):
    statistics = RollCRUD(db).get_roll_statistics(start_date, end_date)
    return statistics
