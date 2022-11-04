from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import schemas, crud
from api.utils import utils
from api.utils.utils import get_db

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)


# generate a list of 5 Stats objects

@router.get("/hourly", response_model=schemas.StatsHourlyResponse)
def read_summaries(start: str, db: Session = Depends(get_db)):
    # return mock data StatsHourlyResponse object
    return utils.generate_stats_hourly_response()
