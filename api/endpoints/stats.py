from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import schemas
from api.utils.validators import validate_date
from api.utils.utils import get_db, generate_stats_hourly_response, generate_device_stats_hourly

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)

@router.get("/hourly", response_model=schemas.StatsHourlyResponse)
def read_summaries(start: str, db: Session = Depends(get_db)):
    if not validate_date(start):
        raise HTTPException(status_code=400, detail="Invalid date format")
    return generate_stats_hourly_response(start)

@router.get("/hourly/device/{id}", response_model=schemas.StatsHourlyResponse)
def read_summaries(start: str, id: int, db: Session = Depends(get_db)):
    if not validate_date(start):
        raise HTTPException(status_code=400, detail="Invalid date format")
    if generate_device_stats_hourly(id, start) is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return generate_device_stats_hourly(id, start)