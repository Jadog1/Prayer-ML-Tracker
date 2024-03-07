from dotenv import load_dotenv
from fastapi import FastAPI
from src.routers.prayerRequests import prayerRequestRouter
from src.dependencies import repositories
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(prayerRequestRouter, prefix="/prayerRequests")

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.on_event("shutdown")
async def shutdown_event():
    repositories.close()
    print("Closed database connection pool")