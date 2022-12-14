from pydantic import BaseModel


class Stats(BaseModel):
    """Schema for stats/ endpoint lists."""
    hour: int
    actualUsage: float
    predictedUsage: float
    price: int


class StatsCreate(BaseModel):
    """Request schema for stats endpoints."""
    fromDateTime: str
    toDateTime: str


class StatsHourlyResponse(BaseModel):
    """Response schema for stats/hourly endpoint."""
    consumption: list[Stats]


class DeviceCreate(BaseModel):
    """Schema for devices/ endpoint request"""
    name: str
    state: int
    interval: int


class DeviceResponse(DeviceCreate):
    """Schema for devices/ endpoint response"""
    id: int
    pass

    class Config:
        orm_mode = True


class DeviceResponseWithConsumption(DeviceResponse):
    """Schema for devices/ endpoint response"""
    consumption: int


class Device(DeviceResponse):
    """Schema for devices/ endpoint lists."""
    pass
    class Config:
        orm_mode = True



class DeviceEnergyConsumptionCreate(BaseModel):
    device_id: int
    consumption: int


class DeviceEnergyConsumption(DeviceEnergyConsumptionCreate):
    """Schema for device_energy_usage/ endpoint request"""
    id: int
    timestamp: int

    class Config:
        orm_mode = True


class TotalDeviceEnergyConsumption(BaseModel):
    """Schema for device_energy_usage/total endpoint response"""
    device_id: int
    device_name: str
    total: int


class ScheduleCreate(BaseModel):
    """Schema for schedules/ endpoint request"""
    device_id: int
    state: int
    start: int


class Schedule(ScheduleCreate):
    """Schema for schedules/ endpoint response"""
    id: int
    class Config:
        orm_mode = True