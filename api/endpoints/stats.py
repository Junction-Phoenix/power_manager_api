from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import schemas, crud
from api.utils.validators import validate_date
from api.utils.utils import get_db, generate_stats_hourly_response


router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)


# generate a list of 5 Stats objects

@router.get("/hourly", response_model=schemas.StatsHourlyResponse)
def read_summaries(start: str, db: Session = Depends(get_db)):
    if not validate_date(start):
        raise HTTPException(status_code=400, detail="Invalid date format")
    return generate_stats_hourly_response()
