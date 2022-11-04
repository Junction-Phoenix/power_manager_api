from pydantic import BaseModel


class Stats(BaseModel):
    """Schema for stats/ endpoint lists."""
    hour: int
    usage: float
    price: int


class StatsRequest(BaseModel):
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

class DeviceResponse(DeviceCreate):
    """Schema for devices/ endpoint response"""
    id: int
    pass

class Device(DeviceResponse):
    """Schema for devices/ endpoint lists."""
    pass
    class Config:
        orm_mode = True

