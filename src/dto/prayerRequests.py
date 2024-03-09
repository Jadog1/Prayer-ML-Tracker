from typing import List
import pandas as pd
from src.repo.orm import PrayerRequestORM

class PrayerRequest():
    def __init__(self, prayerRequest: PrayerRequestORM = None):
        if prayerRequest:
            self.id = prayerRequest.id
            self.account_id = prayerRequest.account_id
            self.contact_id = prayerRequest.contact_id
            self.group_id = prayerRequest.contact.group_id if prayerRequest.contact else None
            self.request = prayerRequest.request
            self.archived_at = prayerRequest.archived_at
            self.name = prayerRequest.contact.name if prayerRequest.contact else None
            self.group = prayerRequest.contact.group.name if prayerRequest.contact.group else None
            self.link_id = prayerRequest.link_id
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'contact_id': self.contact_id,
            'group_id': self.group_id,
            'request': self.request,
            'archived_at': self.archived_at,
            'name': self.name,
            'group': self.group,
            'link_id': self.link_id,
            'id': self.id,
        }
    
    def from_dict(self, data: dict)->'PrayerRequest':
        self.account_id = data.get('account_id')
        self.contact_id = data.get('contact_id')
        self.request = data.get('request')
        self.archived_at = data.get('archived_at')
        self.link_id = data.get('link_id')
        self.id = data.get('id')
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