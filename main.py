from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.framework.app import App
from src.routers.prayerRequests import PrayerRequestRoute
from src.routers.contacts import ContactRoute
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from src.repo.orm import OpenPool
from src.repo.contacts import ContactRepoImpl
from src.repo.prayerRequests import PrayerRequestRepoImpl
from src.models.models import Embeddings, BibleEmbeddings, ClassifierModels

load_dotenv()
pg_uri = os.environ.get('PRAYERS_PG_DATABASE_URL')

print("Loading embeddings")    
embedding_model = Embeddings()
bible_model = BibleEmbeddings()
classifier_models = ClassifierModels()
class Repositories:
    def __init__(self, pg_uri):
        pool = OpenPool(pg_uri)
        self.prayer_request_repo = PrayerRequestRepoImpl(pool, embedding_model, classifier_models)
        self.contact_repo = ContactRepoImpl(pool)
        self.pool = pool

    def close(self):
        self.pool.close()

print("Loading repositories")
repositories = Repositories(pg_uri)

print("Creating FastAPI app")
httpApp = FastAPI()

frameworkApp = App()

prayerRequestRoute = PrayerRequestRoute(frameworkApp, repositories.prayer_request_repo, embedding_model, bible_model)
httpApp.include_router(prayerRequestRoute.router, prefix="/api/prayer_requests")

contactRoute = ContactRoute(frameworkApp, repositories.contact_repo)
httpApp.include_router(contactRoute.router, prefix="/api/contacts")


httpApp.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

@httpApp.on_event("shutdown")
async def shutdown_event():
    repositories.close()
    print("Closed database connection pool")