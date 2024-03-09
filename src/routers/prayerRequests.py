from fastapi import APIRouter
from src.models.models import Embeddings
from ..repo.prayerRequests import PrayerRequestRepoImpl

# At some point in time if we ever want to support multiple accounts, we'll need to use cookies
account_id = 1

class PrayerRequestRoute():
    def __init__(self, repo: PrayerRequestRepoImpl, model: Embeddings):
        self.repo = repo
        self.model = model
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_prayer_requests, methods=["GET"])

    def get_prayer_requests(self):
        results = self.repo.get_all(account_id)
        return results.to_list()