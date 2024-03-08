from abc import ABC, abstractmethod
from ..dto.contacts import Contacts, Contact
from ..dto.groups import Group, Groups
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, Session
from .orm import Base, ContactORM , GroupORM

class ContactRepo(ABC):
    @abstractmethod
    def get_all(self, account_id:int)->Contacts:
         pass
    
    @abstractmethod
    def save_contact(self, account_id:int, contact: Contact):
        pass

    @abstractmethod
    def delete(self, account_id:int, contact_id: int):
        pass

    @abstractmethod
    def save_group(self, account_id:int, group: Group):
        pass

class ContactRepoImpl(ContactRepo):
    def __init__(self, session: scoped_session[Session]):
        self.pool = session

    def get_all(self, account_id:int)->Contacts:
        with self.pool() as session:
            contacts = session.query(ContactORM).filter(ContactORM.account_id == account_id).all()
            return self._to_contacts(contacts)

    def save_contact(self, account_id:int, contact: Contact):
        with self.pool() as session:
            contact.account_id = account_id
            session.add(ContactORM(account_id=account_id, name=contact.name, group_id=contact.group_id))
            session.commit()

    def delete(self, account_id:int, contact_id: int):
        with self.pool() as session:
            result = session.query(ContactORM).filter(ContactORM.account_id == account_id, ContactORM.id == contact_id)
            result.delete()
            session.commit()

    def save_group(self, account_id:int, group: Group):
        with self.pool() as session:
            group.account_id = account_id
            session.add(GroupORM(account_id=account_id, name=group.name))
            session.commit()
        
    def get_groups(self, account_id:int)->Groups:
        with self.pool() as session:
            groups = session.query(GroupORM).filter(GroupORM.account_id == account_id).all()
            return self._to_groups(groups)

    def _to_contacts(self, contacts: List[ContactORM])->Contacts:
        newContacts = Contacts()
        for contact in contacts:
            newContacts.add(Contact(contact))
        return newContacts
    
    def _to_groups(self, groups: List[GroupORM])->Groups:
        newGroups = Groups()
        for group in groups:
            newGroups.add(Group(group))
        return newGroups

