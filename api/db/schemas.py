from pydantic import BaseModel


class Stats(BaseModel):
    """Schema for stats/ endpoint lists."""
    dateTime: str
    totalCost: float
    usage: float
    price: float
    predictedUsage: float
    predictedTotalCost: float


class StatsHourlyRequest(BaseModel):
    """Request schema for stats/hourly endpoint."""
    fromDateTime: str
    toDateTime: str


class StatsHourlyResponse(BaseModel):
    """Response schema for stats/hourly endpoint."""
    dayTotal: float
    dayTotalPredicted: float

    consumption: list[Stats]

    class Config:
        orm_mode = True

