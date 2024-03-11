from fastapi import APIRouter
from src.models.models import Embeddings
from ..repo.prayerRequests import PrayerRequestRepoImpl
from ..dto.prayerRequests import PrayerRequest
from pydantic import BaseModel

# At some point in time if we ever want to support multiple accounts, we'll need to use cookies
account_id = 1

class SaveBaseModel(BaseModel):
    account_id: int
    request: str
    archived_at: str
    link_id: int
    id: int
    contact: dict

class LinkBaseModel(BaseModel):
    id_from: int
    id_to: int

class PrayerRequestRoute():
    def __init__(self, repo: PrayerRequestRepoImpl, model: Embeddings):
        self.repo = repo
        self.model = model
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_all, methods=["GET"])
        self.router.add_api_route("/contact/{contact_id}", self.get_contact, methods=["GET"])
        self.router.add_api_route("/", self.save, methods=["POST"])
        self.router.add_api_route("/{id}", self.delete, methods=["DELETE"])
        self.router.add_api_route("/similar/{id}", self.find_similar, methods=["GET"])
        self.router.add_api_route("/link", self.link_requests, methods=["POST"])

    def get_all(self):
        results = self.repo.get_all(account_id)
        return results.to_list()
    
    def get_contact(self, contact_id: int):
        results = self.repo.get_contact(account_id, contact_id)
        return results.to_list()
    
    def save(self, data: SaveBaseModel):
        prayer = PrayerRequest().from_dict(data)
        self.repo.save(account_id, prayer)
        return prayer.to_dict()
    
    def delete(self, id: int):
        self.repo.delete(account_id, id)
        return {"status": "deleted"}
    
    def find_similar(self, id: int):
        similar = self.repo.get_similar_requests(account_id, id)
        return similar.to_list()
    
    def link_requests(self, link: LinkBaseModel):
        self.repo.save_link(account_id, link.id_from, link.id_to)
        return {"status": "linked"}