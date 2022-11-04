from fastapi import FastAPI

from db import models
from db.database import engine
from endpoints import stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
app.include_router(stats.router)

