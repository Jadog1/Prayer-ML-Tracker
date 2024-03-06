from dotenv import load_dotenv
from fastapi import FastAPI
from src.repo.prayerRequests import PrayerRequestRepoImpl, OpenPGPool
import os

pg_uri = os.environ.get('PRAYERS_PG_DATABASE_URL')


load_dotenv()

app = FastAPI()
prayer_request_repo = PrayerRequestRepoImpl(OpenPGPool(pg_uri))

@app.get("/")
async def root():
    return {"message": "Hello World"}