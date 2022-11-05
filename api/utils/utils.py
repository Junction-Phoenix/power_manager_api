import random

from dotenv import load_dotenv

from api.db import schemas
from api.db.database import SessionLocal
from api.data.overall import overall_stats

load_dotenv()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_stats_list():
    stats_list = []
    for i in range(1, 25):
        stats_list.append(schemas.Stats(hour=i, actualUsage=random.randint(200, 1000), predictedUsage=random.randint(200,1000), price=random.randint(23, 38)))
    return stats_list


# generate StatsHourlyResponse object
def generate_stats_hourly_response(date):
    if date in ["2022-11-03", "2022-11-04", "2022-11-05"]:
        stats_list = overall_stats[date]
        return schemas.StatsHourlyResponse(**stats_list)

    stats_hourly_response = schemas.StatsHourlyResponse(consumption=generate_stats_list())
    return stats_hourly_response

def get_device_consumption_by_id_and_date(device_id, date):
    return 0