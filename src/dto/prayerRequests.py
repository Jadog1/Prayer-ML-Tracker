from typing import List
import pandas as pd
from src.models.models import EmbeddingResult
from src.repo.orm import PrayerRequestORM

class PrayerRequest():
    def __init__(self, prayerRequest: PrayerRequestORM | dict = None, includeEmbeddings: bool = False):
        if prayerRequest:
            self.id = prayerRequest.id
            self.account_id = prayerRequest.account_id
            self.contact_id = prayerRequest.contact_id
            self.request = prayerRequest.request
            self.archived_at = prayerRequest.archived_at
            if type(prayerRequest.contact) == dict:
                self.group_id = prayerRequest.contact['group_id'] if prayerRequest.contact else None
                self.name = prayerRequest.contact['name'] if prayerRequest.contact else None
                self.group = prayerRequest.contact['group']['name'] if prayerRequest.contact['group'] else None
            else:
                self.group_id = prayerRequest.contact.group_id
                self.name = prayerRequest.contact.name
                self.group = prayerRequest.contact.group.name
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
            'contact': {
                'id': self.contact_id,
                'name': self.name,
                'group': {
                    'id': self.group_id,
                    'name': self.group
                }
            },
            'request': self.request,
            'archived_at': self.archived_at,
            'link_id': self.link_id,
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sentiment': self.sentiment,
            'emotion': self.emotion,
            'prayer_type': self.prayer_type
        }
    
    def from_dict(self, data: dict)->'PrayerRequest':
        self.account_id = data.get('account_id')
        self.request = data.get('request')
        self.archived_at = data.get('archived_at') if data.get('archived_at') != '' else None
        self.link_id = data.get('link_id') if data.get('link_id') != 0 else None
        id = data.get('id')
        self.id = id if id is not None and id > 0 else None
        if data.get('contact'):
            self.contact_id = data['contact'].get('id')
            self.name = data['contact'].get('name')
            if data['contact'].get('group'):
                self.group_id = data['contact']['group'].get('id')
                self.group = data['contact']['group'].get('name')
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