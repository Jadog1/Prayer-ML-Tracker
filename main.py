from dotenv import load_dotenv
from fastapi import FastAPI
from src.routers.prayerRequests import prayerRequestRouter
from src.dependencies import repositories

app = FastAPI()

app.include_router(prayerRequestRouter, prefix="/prayerRequests")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("shutdown")
async def shutdown_event():
    repositories.close()
    print("Closed database connection pool")