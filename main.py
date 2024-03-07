from dotenv import load_dotenv
from fastapi import FastAPI
from src.routers.prayerRequests import prayerRequestRouter

load_dotenv()

app = FastAPI()

app.include_router(prayerRequestRouter, prefix="/prayerRequests")

@app.get("/")
async def root():
    return {"message": "Hello World"}

