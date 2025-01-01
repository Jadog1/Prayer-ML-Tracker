from typing import List
import pandas as pd
from src.dto.contacts import Contact
from src.models.models import EmbeddingResult
from src.repo.orm import PrayerRequestORM

class PrayerRequest():
    def __init__(self, prayerRequest: PrayerRequestORM | dict = None, includeEmbeddings: bool = False):
        if prayerRequest:
            self.id = prayerRequest.id
            self.account_id = prayerRequest.account_id
            self.contact_group_id = prayerRequest.contact_group_id
            self.request = prayerRequest.request
            self.archived_at = prayerRequest.archived_at
            if type(prayerRequest.contact_group) == dict:
                self.name = prayerRequest.contact_group.contact['name'] if prayerRequest.contact_group else None
                self.contact_id = prayerRequest.contact_group.contact['id'] if prayerRequest.contact_group else None
            else:
                self.contact = Contact(prayerRequest.contact_group.contact).to_dict()
            self.link_id = prayerRequest.link_id
            self.created_at = prayerRequest.created_at
            self.updated_at = prayerRequest.updated_at
            self.sentiment = prayerRequest.sentiment_analysis
            self.emotion = prayerRequest.emotion_roberta
            self.prayer_type = prayerRequest.prayer_type
            self.topics = [pt.topic.name for pt in prayerRequest.prayer_topics ]
            if includeEmbeddings:
                self.embeddings = EmbeddingResult(prayerRequest.gte_base_embedding, prayerRequest.msmarco_base_embedding)
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'contact': self.contact,
            'request': self.request,
            'archived_at': self.archived_at,
            'link_id': self.link_id,
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sentiment': self.sentiment,
            'emotion': self.emotion,
            'prayer_type': self.prayer_type,
            'topics': self.topics
        }
    
    def from_dict(self, data: dict)->'PrayerRequest':
        self.account_id = data.get('account_id')
        self.request = data.get('request')
        self.archived_at = data.get('archived_at') if data.get('archived_at') != '' else None
        self.link_id = data.get('link_id') if data.get('link_id') != 0 else None
        id = data.get('id')
        self.id = id if id is not None and id > 0 else None
        if data.get('contact'):
            self.contact_group_id = data['contact'].get('id')
            self.name = data['contact'].get('name')
        return self

class PrayerRequests():
    def __init__(self):
        self.prayerRequests: List[PrayerRequest] = []

    def add(self, prayer: PrayerRequest):
        self.prayerRequests.append(prayer)
    
    def to_dataframe(self):
        rows = []
        for prayer in self.prayerRequests:
            rows.append(prayer.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [prayer.to_dict() for prayer in self.prayerRequests]
    
    def from_list(self, data: List[dict]):
        for prayer in data:
            self.add(PrayerRequest().from_dict(prayer))
        return self