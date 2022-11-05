from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import schemas, crud
from api.utils.utils import get_db, get_single_device_consumption, get_mock_device_consumption
from api.utils.validators import validate_date

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={404: {"description": "Not found"}},
)


# generate a list of 5 Stats objects

@router.post("", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db=db, device=device)


@router.get("", response_model=list[schemas.Device])
def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices


@router.get("/with_consumption", response_model=list[schemas.DeviceResponseWithConsumption])
def get_device_with_consumption(date: str, db: Session = Depends(get_db)):
    if not validate_date(date):
        raise HTTPException(status_code=400, detail="Invalid date format")
    devices = crud.get_devices(db)
    response = []
    for device in devices:
        response.append(schemas.DeviceResponseWithConsumption(id=device.id,
                                                              name=device.name,
                                                              state=device.state,
                                                              interval=device.interval,
                                                              consumption=get_single_device_consumption()))
    return response + get_mock_device_consumption(date)


@router.get("/state/{device_id}", response_model=str)
def get_device_state(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device.state


@router.get("/{device_id}", response_model=schemas.Device)
def get_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@router.put("/{device_id}", response_model=schemas.Device)
def update_device(device_id: int, device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return crud.update_device(db=db, device_id=device_id, device=device)


@router.delete("/{device_id}", response_model=schemas.Device)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return crud.delete_device(db=db, device_id=device_id)
