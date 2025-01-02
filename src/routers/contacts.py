from fastapi import APIRouter, HTTPException

from src.dto.contacts import Contact
from src.dto.groups import Group
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
        self.router.add_api_route("/", self.add_contact, methods=["POST"])
        self.router.add_api_route("/groups", self.get_groups, methods=["GET"])
        self.router.add_api_route("/groups/{contact_id}", self.get_groups_for_contact, methods=["GET"])
        self.router.add_api_route("/groups", self.save_group, methods=["POST"])
        self.router.add_api_route("/groups/{group_id}", self.delete_group, methods=["DELETE"])
        self.router.add_api_route("/contact_groups", self.get_contact_groups, methods=["GET"])
        self.router.add_api_route("/contact_groups", self.add_contact_to_group, methods=["POST"])
        self.router.add_api_route("/contact_groups", self.delete_contact_from_group, methods=["DELETE"])
        self.router.add_api_route("/{contact_id}", self.delete_contact, methods=["DELETE"])

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
    
    def save_group(self, data: dict):
        group = Group().from_dict(data)
        try:
            newId = self.repo.save_group(account_id, group)
        except Exception as e:
            self.app.Logger().error(f"Error saving group: {e}", error=e, data=group.to_dict())
            raise HTTPException(status_code=400, detail="Error saving group")
        return {"id": newId}
    
    def delete_contact_from_group(self, contact_id: int, group_id: int):
        try:
            self.repo.delete_contact_from_group(account_id, contact_id, group_id)
        except Exception as e:
            self.app.Logger().error(f"Error deleting contact from group: {e}", error=e, data={"contact_id": contact_id, "group_id": group_id})
            raise HTTPException(status_code=400, detail="Error deleting contact from group")
        
    def add_contact_to_group(self, data: dict):
        contact_id = data.get('contact_id')
        group_id = data.get('group_id')
        try:
            self.repo.add_contact_to_group(account_id, contact_id, group_id)
        except Exception as e:
            self.app.Logger().error(f"Error adding contact to group: {e}", error=e, data={"contact_id": contact_id, "group_id": group_id})
            raise HTTPException(status_code=400, detail="Error adding contact to group")
        
    def delete_contact(self, contact_id: int):
        try:
            self.repo.delete(account_id, contact_id)
        except Exception as e:
            self.app.Logger().error(f"Error deleting contact: {e}", error=e, data={"contact_id": contact_id})
            raise HTTPException(status_code=400, detail="Error deleting contact")
    
    def delete_group(self, group_id: int):
        try:
            self.repo.deleteGroup(account_id, group_id)
        except Exception as e:
            self.app.Logger().error(f"Error deleting group: {e}", error=e, data={"group_id": group_id})
            raise HTTPException(status_code=400, detail="Error deleting group")
        
    def get_groups_for_contact(self, contact_id: int):
        results = self.repo.get_groups_for_contact(account_id, contact_id)
        return results.to_list()