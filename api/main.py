from fastapi import FastAPI

from api.endpoints import devices
from db import models
from db.database import engine
from endpoints import stats
import pkg_resources

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Power management API", description="API for the power management APP project", version=pkg_resources.get_distribution("power-manager-api").version)

# Dependency
app.include_router(stats.router)
app.include_router(devices.router)

