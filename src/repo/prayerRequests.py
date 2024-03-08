from abc import ABC, abstractmethod
from ..dto.prayerRequests import PrayerRequest, PrayerRequests
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from .orm import Base, PrayerRequestORM as ORMPrayerRequest, LinkORM

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
        
class PrayerRequestRepoImpl(PrayerRequestRepo):
    def __init__(self, session: scoped_session[Session]):
        self.pool = session

    def get_all(self, account_id:int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(ORMPrayerRequest).filter(ORMPrayerRequest.account_id == account_id).all()
            return self._to_prayer_requests(requests)

    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(ORMPrayerRequest).filter(ORMPrayerRequest.account_id == account_id, ORMPrayerRequest.contact_id == contact_id).all()
            return self._to_prayer_requests(requests)

    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(ORMPrayerRequest).filter(ORMPrayerRequest.account_id == account_id, ORMPrayerRequest.created_at >= start, ORMPrayerRequest.created_at <= end).all()
            return self._to_prayer_requests(requests)

    def save(self, account_id:int, request: PrayerRequest):
        with self.pool() as session:
            session.add(ORMPrayerRequest(account_id=account_id, contact_id=request.contact_id, request=request.request, archived_at=request.archived_at, link_id=request.link_id))
            session.commit()

    def save_link(self, link_id:int):
        with self.pool() as session:
            session.add(LinkORM())
            session.commit()

    def _to_prayer_requests(self, requests: List[ORMPrayerRequest])->PrayerRequests:
        prayer_requests = PrayerRequests()
        for request in requests:
            prayer_requests.add(PrayerRequest(request))
        return prayer_requests