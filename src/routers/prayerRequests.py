from fastapi import APIRouter, Depends
from ..repo.prayerRequests import PrayerRequestRepoImpl
from ..dependencies import get_repositories, Repositories

prayerRequestRouter = APIRouter()

account_id = 1

@prayerRequestRouter.get("/")
async def get_prayer_requests(repos: Repositories = Depends(get_repositories)):
    return await repos.prayer_request_repo.get_all(account_id)