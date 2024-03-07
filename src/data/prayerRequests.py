from typing import List
import pandas as pd
from src.repo.orm import PrayerRequestORM

class PrayerRequest():
    def __init__(self, prayerRequest: PrayerRequestORM = None):
        self.account_id = prayerRequest.account_id
        self.contact_id = prayerRequest.contact_id
        self.group_id = prayerRequest.contact.group_id if prayerRequest.contact else None
        self.request = prayerRequest.request
        self.archived_at = prayerRequest.archived_at
        self.name = prayerRequest.contact.name if prayerRequest.contact else None
        self.group = prayerRequest.contact.group.name if prayerRequest.contact.group else None
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'contact_id': self.contact_id,
            'group_id': self.group_id,
            'request': self.request,
            'archived_at': self.archived_at,
            'name': self.name,
            'group': self.group
        }

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