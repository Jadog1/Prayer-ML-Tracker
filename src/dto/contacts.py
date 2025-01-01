from typing import List
import pandas as pd
from src.repo.orm import ContactGroupORM, ContactORM

class Contact():
    def __init__(self, contact: ContactORM = None):
        if contact:
            self.id = contact.id
            self.account_id = contact.account_id
            self.name = contact.name
            self.description = contact.description
            self.created_at = contact.created_at
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'name': self.name,
            'id': self.id,
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict)->'Contact':
        self.account_id = data.get('account_id')
        self.name = data.get('name')
        self.id = data.get('id')
        self.created_at = data.get('created_at')
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
    

class ContactGroup():
    def __init__(self, contact_group: ContactGroupORM = None):
        if contact_group:
            self.id = contact_group.id
            self.contact_id = contact_group.contact_id
            self.group_id = contact_group.group_id
            self.created_at = contact_group.created_at
    
    def to_dict(self):
        return {
            'contact_id': self.contact_id,
            'group_id': self.group_id,
            'id': self.id,
            'created_at': self.created_at
        }
    
    def from_dict(self, data: dict)->'ContactGroup':
        self.contact_id = data.get('contact_id')
        self.group_id = data.get('group_id')
        self.id = data.get('id')
        self.created_at = data.get('created_at')
        return self
    
class ContactGroups():
    def __init__(self):
        self.contactGroups: List[ContactGroup] = []

    def add(self, contactGroup: ContactGroup):
        self.contactGroups.append(contactGroup)
    
    def to_dataframe(self):
        rows = []
        for contactGroup in self.contactGroups:
            rows.append(contactGroup.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [contactGroup.to_dict() for contactGroup in self.contactGroups]
    
    def from_list(self, data: List[dict]):
        for contactGroup in data:
            self.add(ContactGroup().from_dict(contactGroup))
        return self