from fastapi import FastAPI

from api.endpoints import devices
from db import models
from db.database import engine
from endpoints import stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Power management API", description="API for the power management APP project")

# Dependency
app.include_router(stats.router)
app.include_router(devices.router)

