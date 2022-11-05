from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String)
    state = Column(String)
    interval = Column(Integer)
    device_energy_consumption = relationship("DeviceEnergyConsumption")

class DeviceEnergyConsumption(Base):
    __tablename__ = "device_energy_consumption"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"))
    consumption = Column(Integer)
    # unix timestamp
    timestamp = Column(Float)
    device = relationship("Device", back_populates="device_energy_consumption")

class Schedule(Base):
    __tablename__ = "schedules.py"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"))
    state = Column(Integer)
    start = Column(Integer)
    device = relationship("Device")