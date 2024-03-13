from fastapi import APIRouter

from src.framework.app import App
from ..repo.contacts import ContactRepoImpl

# At some point in time if we ever want to support multiple accounts, we'll need to use cookies
account_id = 1

class ContactRoute():
    def __init__(self, app:App, repo: ContactRepoImpl):
        self.app = app
        self.repo = repo
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_contacts, methods=["GET"])
        self.router.add_api_route("/groups", self.get_groups, methods=["GET"])

    def get_contacts(self):
        results = self.repo.get_all(account_id)
        return results.to_list()
    
    def get_groups(self):
        results = self.repo.get_groups(account_id)
        return results.to_list()