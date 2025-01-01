from fastapi import APIRouter, HTTPException

from src.dto.contacts import Contact
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
        self.router.add_api_route("/", self.add_contact, methods=["POST"])
        self.router.add_api_route("/contact_groups", self.get_contact_groups, methods=["GET"])

    def get_contacts(self):
        results = self.repo.get_all(account_id)
        return results.to_list()
    
    def get_groups(self):
        results = self.repo.get_groups(account_id)
        return results.to_list()

    def get_contact_groups(self):
        results = self.repo.get_all_contact_groups(account_id)
        return results.to_list()
    
    def add_contact(self, data: dict):
        contact = Contact().from_dict(data)
        try:
            newId = self.repo.save_contact(account_id, contact)
        except Exception as e:
            self.app.Logger().error(f"Error saving contact: {e}", error=e, data=contact.to_dict())
            raise HTTPException(status_code=400, detail="Error saving contact")
        return {"id": newId}