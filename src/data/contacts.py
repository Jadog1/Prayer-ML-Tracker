from typing import List
import pandas as pd
from src.repo.orm import ContactORM

class Contact():
    def __init__(self, contact: ContactORM = None):
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