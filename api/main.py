from fastapi import FastAPI
from api.db import crud, schemas
from api.db.crud import update_device, delete_schedule, get_all_schedules
from api.endpoints import devices, devices_consumption, schedules
from db import models
from db.database import engine, fast_api_sessionmaker
from endpoints import stats
import pkg_resources
from fastapi_utils.tasks import repeat_every

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Power management API", description="API for the power management APP project", version=pkg_resources.get_distribution("power-manager-api").version)
sessionmaker = fast_api_sessionmaker

# Dependency
app.include_router(stats.router)
app.include_router(devices.router)
app.include_router(devices_consumption.router)
app.include_router(schedules.router)


@app.on_event("startup")
@repeat_every(seconds=1, raise_exceptions=True)
def update_device_state():
    with sessionmaker.context_session() as db:
        schedules = get_all_schedules(db, skip=0, limit=100)
        for schedule in schedules:
            device = crud.get_device(db, schedule.device_id)
            device_request = schemas.DeviceCreate(state=schedule.state, name=device.name, interval=device.interval)
            update_device(db=db, device_id=schedule.device_id, device=device_request)
        for schedule in schedules:
            delete_schedule(db=db, schedule_id=schedule.id)
            db.commit()




