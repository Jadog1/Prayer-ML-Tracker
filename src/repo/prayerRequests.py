from abc import ABC, abstractmethod
from ..dto.prayerRequests import PrayerRequest, PrayerRequests
from typing import List
from sqlalchemy.orm import scoped_session, Session
from .orm import PrayerRequestORM, LinkORM
from ..models.models import Embeddings

class PrayerRequestRepo(ABC):
    @abstractmethod
    def get_all(self, account_id:int)->PrayerRequests:
        pass

    @abstractmethod
    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        pass

    @abstractmethod
    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        pass

    @abstractmethod
    def save(self, account_id:int, request: PrayerRequest):
        pass

    @abstractmethod
    def save_link(self, link_id:int):
        pass
        
class PrayerRequestRepoImpl(PrayerRequestRepo):
    def __init__(self, session: scoped_session[Session], model: Embeddings):
        self.pool = session
        self.model = model

    def get_all(self, account_id:int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id).all()
            return self._to_prayer_requests(requests)

    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id, PrayerRequestORM.contact_id == contact_id).all()
            return self._to_prayer_requests(requests)

    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(
                PrayerRequestORM.account_id == account_id, 
                PrayerRequestORM.created_at >= start, PrayerRequestORM.created_at <= end).all()
            return self._to_prayer_requests(requests)

    def save(self, account_id:int, request: PrayerRequest):
        with self.pool() as session:
            request.account_id = account_id
            ormRequest = PrayerRequestORM(
                id=request.id, account_id=account_id, contact_id=request.contact_id, 
                request=request.request, archived_at=request.archived_at, link_id=request.link_id)
            self._set_embeddings(ormRequest)
            session.merge(ormRequest)
            session.commit()

    def _set_embeddings(self, prayer_request: PrayerRequestORM):
        embeddings = self.model.calculate_embeddings(prayer_request.request)
        prayer_request.gte_base_embedding = embeddings.get_gte_base()
        prayer_request.msmarco_base_embedding = embeddings.get_msmarco_base()

    def save_link(self, link_id:int):
        with self.pool() as session:
            session.add(LinkORM())
            session.commit()

    def _to_prayer_requests(self, requests: List[PrayerRequestORM])->PrayerRequests:
        prayer_requests = PrayerRequests()
        for request in requests:
            prayer_requests.add(PrayerRequest(request))
        return prayer_requests