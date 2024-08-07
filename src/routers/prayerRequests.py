from fastapi import APIRouter, HTTPException
from src.framework.app import App
from src.models.models import BibleEmbeddings, Embeddings
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

class SummaryBaseModel(BaseModel):
    date_from: str
    date_to: str
    group_id: int


class PrayerRequestRoute():
    def __init__(self, app: App, repo: PrayerRequestRepoImpl, model: Embeddings, bibleModel: BibleEmbeddings):
        self.app = app
        self.repo = repo
        self.model = model
        self.bibleModel = bibleModel
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_all, methods=["GET"])
        self.router.add_api_route("/{id}", self.get, methods=["GET"])
        # /links should have 2 parameters, link_id and request_id
        self.router.add_api_route("/links/", self.get_links, methods=["GET"])
        self.router.add_api_route("/contact/{contact_id}", self.get_contact, methods=["GET"])
        self.router.add_api_route("/", self.save, methods=["POST"])
        self.router.add_api_route("/", self.update, methods=["PUT"])
        self.router.add_api_route("/{id}", self.delete, methods=["DELETE"])
        self.router.add_api_route("/similar/{id}", self.find_similar, methods=["GET"])
        self.router.add_api_route("/similar/bible/{id}", self.find_similar_bible_verses, methods=["GET"])
        self.router.add_api_route("/link", self.link_requests, methods=["POST"])
        self.router.add_api_route("/summary", self.get_summary, methods=["POST"])

    def get_all(self):
        results = self.repo.get_all(account_id)
        return results.to_list()
    
    def get_contact(self, contact_id: int):
        results = self.repo.get_contact(account_id, contact_id)
        return results.to_list()
    
    def get(self, id: int):
        result = self.repo.get(account_id, id)
        return result.to_dict()
    
    def get_links(self, request_id: int, link_id: int):
        results = self.repo.get_linked_requests(account_id, request_id, link_id)
        return results.to_list()
    
    def get_summary(self, summary: SummaryBaseModel):
        if summary.group_id == 0:
            summary.group_id = None
        prayers = self.repo.get_group_session(account_id, summary.date_from, summary.date_to, summary.group_id)
        prayerList = prayers.to_list()
        prayer_request_ids = [prayer['id'] for prayer in prayerList]
        topics = self.repo.get_group_session_topics(prayer_request_ids=prayer_request_ids)
        return {
            "prayers": prayerList,
            "topics": topics.to_list()
        }
    
    def save(self, data: dict):
        prayer = PrayerRequest().from_dict(data)
        try:
            result = self.repo.save(account_id, prayer)
        except Exception as e:
            self.app.Logger().error(f"Error saving prayer request: {e}", error=e, data=prayer.to_dict())
            raise HTTPException(status_code=400, detail="Error saving prayer request")
        return result.to_dict()
    
    def update(self, data: dict):
        prayer = PrayerRequest().from_dict(data)
        try:
            result = self.repo.update(account_id, prayer)
        except Exception as e:
            self.app.Logger().error(f"Error updating prayer request: {e}", error=e, data=prayer.to_dict())
            raise HTTPException(status_code=400, detail="Error updating prayer request")
        return result.to_dict()
    
    def delete(self, id: int):
        self.repo.delete(account_id, id)
        return {"status": "deleted"}
    
    def find_similar(self, id: int):
        if id == 0:
            raise HTTPException(status_code=400, detail="id cannot be 0")
        similar = self.repo.get_similar_requests(account_id, id)
        return similar.to_list()
    
    def find_similar_bible_verses(self, id: int):
        if id == 0:
            raise HTTPException(status_code=400, detail="id cannot be 0")
        similar = self.repo.get_similar_verses(account_id, id)
        # embedding = self.repo.get(account_id, id, include_embeddings=True).embeddings
        # similar = self.bibleModel.search_verses(embedding, 5)
        return similar
    
    def link_requests(self, link: LinkBaseModel):
        self.repo.link_requests(account_id, link.id_from, link.id_to)
        return {"status": "linked"}