import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import schemas, crud
from api.utils.utils import get_db

router = APIRouter(
    prefix="/devices/consumption",
    tags=["consumption"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.DeviceEnergyConsumption)
def create_device_consumption(consumption: schemas.DeviceEnergyConsumptionCreate, db: Session = Depends(get_db)):
    # check if device exists
    if not crud.get_device(db, device_id=consumption.device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    return crud.create_device_energy_consumption(db=db, device_energy_consumption=consumption)


# get total of all device energy consumption for a specific device and query between two unix timestamps for all devices
@router.get("/total", response_model=list[schemas.TotalDeviceEnergyConsumption])
def device_consumption_total(start: int, end: int, db: Session = Depends(get_db)):
    response = []
    devices = crud.get_devices(db)
    for device in devices:
        response.append(schemas.TotalDeviceEnergyConsumption(
            device_id=device.id,
            total=get_single_device_consumption_total(device_id=device.id, start=start, end=end, db=db),
            device_name=device.name
        ))
    return response


# get device energy consumption for a specific device and query between two unix timestamps
@router.get("/{device_id}", response_model=list[schemas.DeviceEnergyConsumption])
def get_device_consumption(device_id: int, start: int, end: int, db: Session = Depends(get_db)) -> list[schemas.DeviceEnergyConsumption]:
    db_consumption = crud.get_device_energy_consumption(db, device_id=device_id, start=start, end=end)
    if db_consumption is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_consumption


# get total of all device energy consumption for a specific device and query between two unix timestamps
@router.get("/{device_id}/total", response_model=int)
def get_single_device_consumption_total(device_id: int, start: int, end: int, db: Session = Depends(get_db)):
    entries = get_device_consumption(device_id, start, end, db)
    return sum([entry.consumption for entry in entries])


