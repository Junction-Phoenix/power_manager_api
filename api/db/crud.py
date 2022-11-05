import calendar
import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()


def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def update_device(db: Session, device_id: int, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def delete_device(db: Session, device_id: int):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    db.delete(db_device)
    db.commit()
    return db_device

def create_device_energy_consumption(db: Session, device_energy_consumption: schemas.DeviceEnergyConsumptionCreate) -> models.DeviceEnergyConsumption:
    unix_time = datetime.datetime.utcnow().timestamp()
    db_device_energy_consumption = models.DeviceEnergyConsumption(**device_energy_consumption.dict(), timestamp=unix_time)
    db.add(db_device_energy_consumption)
    db.commit()
    db.refresh(db_device_energy_consumption)
    return db_device_energy_consumption


# get device energy consumption for a specific device and query between two unix timestamps
def get_device_energy_consumption(db: Session, device_id: int, start: int, end: int) -> list:
    return db.query(models.DeviceEnergyConsumption).filter(models.DeviceEnergyConsumption.device_id == device_id).filter(models.DeviceEnergyConsumption.timestamp >= start).filter(models.DeviceEnergyConsumption.timestamp <= end).all()
