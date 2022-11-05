from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import schemas, crud
from api.db.crud import update_device, get_all_schedules
from api.utils.utils import get_db

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
    responses={404: {"description": "Not found"}},
)

@router.get("/update", response_model=None)
def update_device_state(db: Session = Depends(get_db)):
    schedules = get_all_schedules(db, skip=0, limit=100)
    for schedule in schedules:
        device = crud.get_device(db, schedule.device_id)
        device_request = schemas.DeviceCreate(state=schedule.state, name=device.name, interval=device.interval)
        update_device(db=db, device_id=schedule.device_id, device=device_request)
        delete_schedule(db=db, schedule_id=schedule.id)
        db.commit()
    return None

@router.post("", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    if not crud.get_device(db, device_id=schedule.device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return crud.create_schedule(db=db, schedule=schedule)


@router.get("", response_model=list[schemas.Schedule])
def get_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schedules = crud.get_all_schedules(db, skip=skip, limit=limit)
    return schedules


@router.get("/{schedule_id}", response_model=schemas.Schedule)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule


@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return crud.update_schedule(db=db, schedule_id=schedule_id, schedule=schedule)


@router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = crud.get_schedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return crud.delete_schedule(db=db, schedule_id=schedule_id)
