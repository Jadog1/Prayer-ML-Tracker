from typing import List
import pandas as pd
from src.repo.orm import ContactORM

class Contact():
    def __init__(self, contact: ContactORM = None):
        if contact:
            self.account_id = contact.account_id
            self.name = contact.name
            self.group_id = contact.group_id
            self.group = contact.group.name if contact.group else None
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'name': self.name,
            'group_id': self.group_id,
            'group': self.group
        }
    
    def from_dict(self, data: dict)->'Contact':
        self.account_id = data.get('account_id')
        self.name = data.get('name')
        self.group_id = data.get('group_id')
        self.group = data.get('group')
        return self
    
class Contacts():
    def __init__(self):
        self.contacts: List[Contact] = []

    def add(self, contact: Contact):
        self.contacts.append(contact)
    
    def to_dataframe(self):
        rows = []
        for contact in self.contacts:
            rows.append(contact.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [contact.to_dict() for contact in self.contacts]