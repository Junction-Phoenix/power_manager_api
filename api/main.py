from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session

from api.db.crud import get_schedules, get_device
from api.endpoints import devices, devices_consumption, schedules
from api.utils.utils import get_db
from db import models
from db.database import engine
from endpoints import stats
import pkg_resources
from fastapi_utils.tasks import repeat_every

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Power management API", description="API for the power management APP project", version=pkg_resources.get_distribution("power-manager-api").version)

# Dependency
app.include_router(stats.router)
app.include_router(devices.router)
app.include_router(devices_consumption.router)
app.include_router(schedules.router)



@app.on_event("startup")
@repeat_every(seconds=60)
def update_device_state(db: Session = Depends(get_db)):
    schedules = get_schedules()
    for schedule in schedules:
        get_device(schedule.device_id).state = schedule.state
        db.commit()



