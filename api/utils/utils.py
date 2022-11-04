import os
from youtube_transcript_api import YouTubeTranscriptApi as Transcript
import openai
from dotenv import load_dotenv

from api.db import schemas
from api.db.database import SessionLocal

load_dotenv()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_stats_list():
    stats_list = []
    for i in range(5):
        stats_list.append(schemas.Stats(dateTime="2021-01-01T00:00:00Z", totalCost=0.0, usage=0.0, price=0.0, predictedUsage=0.0, predictedTotalCost=0.0))
    return stats_list


# generate StatsHourlyResponse object
def generate_stats_hourly_response():
    stats_hourly_response = schemas.StatsHourlyResponse(dayTotal=0.0, dayTotalPredicted=0.0, consumption=generate_stats_list())
    return stats_hourly_response