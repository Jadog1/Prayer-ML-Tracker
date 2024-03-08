from dotenv import load_dotenv
from fastapi import FastAPI
from src.routers.prayerRequests import PrayerRequestRoute
from src.routers.contacts import ContactRoute
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from src.repo.orm import OpenPool
from src.repo.contacts import ContactRepoImpl
from src.repo.prayerRequests import PrayerRequestRepoImpl

load_dotenv()
pg_uri = os.environ.get('PRAYERS_PG_DATABASE_URL')

class Repositories:
    def __init__(self, pg_uri):
        pool = OpenPool(pg_uri)
        self.prayer_request_repo = PrayerRequestRepoImpl(pool)
        self.contact_repo = ContactRepoImpl(pool)
        self.pool = pool

    def close(self):
        self.pool.close()

repositories = Repositories(pg_uri)

app = FastAPI()

prayerRequestRoute = PrayerRequestRoute(repositories.prayer_request_repo)
app.include_router(prayerRequestRoute.router, prefix="/prayerRequests")

contactRoute = ContactRoute(repositories.contact_repo)
app.include_router(contactRoute.router, prefix="/contacts")


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

@app.on_event("shutdown")
async def shutdown_event():
    repositories.close()
    print("Closed database connection pool")