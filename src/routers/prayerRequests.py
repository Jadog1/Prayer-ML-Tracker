from fastapi import APIRouter, Depends
from ..repo.prayerRequests import PrayerRequestRepoImpl

prayerRequestRouter = APIRouter()

account_id = 1

class PrayerRequestRoute():
    def __init__(self, repo: PrayerRequestRepoImpl):
        self.repo = repo
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_prayer_requests, methods=["GET"])

    def get_prayer_requests(self):
        results = self.repo.get_all(account_id)
        return results.to_list()