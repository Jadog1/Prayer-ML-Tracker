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
from src.models.models import Embeddings

load_dotenv()
pg_uri = os.environ.get('PRAYERS_PG_DATABASE_URL')

print("Loading embeddings")    
embedding_model = Embeddings()
class Repositories:
    def __init__(self, pg_uri):
        pool = OpenPool(pg_uri)
        self.prayer_request_repo = PrayerRequestRepoImpl(pool, embedding_model)
        self.contact_repo = ContactRepoImpl(pool)
        self.pool = pool

    def close(self):
        self.pool.close()

print("Loading repositories")
repositories = Repositories(pg_uri)

print("Creating FastAPI app")
app = FastAPI()

prayerRequestRoute = PrayerRequestRoute(repositories.prayer_request_repo, embedding_model)
app.include_router(prayerRequestRoute.router, prefix="/prayerRequests")

contactRoute = ContactRoute(repositories.contact_repo)
app.include_router(contactRoute.router, prefix="/contacts")


app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

@app.on_event("shutdown")
async def shutdown_event():
    repositories.close()
    print("Closed database connection pool")