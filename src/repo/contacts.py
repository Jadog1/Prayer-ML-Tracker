from abc import ABC, abstractmethod
from ..dto.contacts import ContactGroup, ContactGroups, Contacts, Contact
from ..dto.groups import Group, Groups
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.dialects.postgresql import insert
from .orm import Base, ContactGroupORM, ContactORM , GroupORM

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

    def save_contact(self, account_id:int, contact: Contact, group_id:int):
        with self.pool() as session:
            contact.account_id = account_id
            contactOrm = ContactORM(account_id=contact.account_id, name=contact.name, created_at=contact.created_at)
            session.add(contactOrm)
            session.flush()
            contact_id = contactOrm.id
            session.commit()
            if group_id :
                # Insert a contactGroupORM record if it doesn't already exist for the group/contact pair
                insert_stmt = insert(ContactGroupORM).values(contact_id=contact_id, group_id=group_id).on_conflict_do_nothing()
                session.execute(insert_stmt)


    def delete(self, account_id:int, contact_id: int):
        with self.pool() as session:
            result = session.query(ContactORM).filter(ContactORM.account_id == account_id, ContactORM.id == contact_id)
            result.delete()
            session.commit()

    def delete_contact_from_group(self, account_id:int, contact_id: int, group_id: int):
        with self.pool() as session:
            result = session.query(ContactGroupORM).join(ContactORM).join(GroupORM).filter(
                ContactGroupORM.contact_id == contact_id, ContactGroupORM.group_id == group_id, 
                GroupORM.account_id == account_id, ContactORM.account_id == account_id)
            result.delete()
            session.commit()

    def deleteGroup(self, account_id:int, group_id: int):
        with self.pool() as session:
            result = session.query(ContactGroupORM).filter(ContactGroupORM.group_id == group_id, GroupORM.account_id == account_id)
            result.delete()
            result = session.query(GroupORM).filter(GroupORM.account_id == account_id, GroupORM.id == group_id)
            result.delete()
            session.commit()

    def save_group(self, account_id:int, group: Group):
        with self.pool() as session:
            group.account_id = account_id
            groupOrm = GroupORM(account_id=group.account_id, name=group.name, description=group.description)
            if group.id > 0:
                groupOrm.id = group.id
            session.add(groupOrm)
            session.flush()
            group_id = groupOrm.id
            session.commit()
            return group_id

    def add_contact_to_group(self, account_id:int, contact_id:int, group_id:int):
        with self.pool() as session:
            related_group = session.query(GroupORM).filter(GroupORM.account_id == account_id, GroupORM.id == group_id).first()
            related_contact = session.query(ContactORM).filter(ContactORM.account_id == account_id, ContactORM.id == contact_id).first()
            if not related_group or not related_contact:
                raise ValueError("Group or contact not found")
            insert_stmt = insert(ContactGroupORM).values(contact_id=contact_id, group_id=group_id).on_conflict_do_nothing()
            session.execute(insert_stmt)
        
    def get_groups(self, account_id:int)->Groups:
        with self.pool() as session:
            groups = session.query(GroupORM).filter(GroupORM.account_id == account_id).all()
            return self._to_groups(groups)
        
    def get_groups_for_contact(self, account_id:int, contact_id:int)->Groups:
        with self.pool() as session:
            groups = session.query(GroupORM).join(ContactGroupORM).filter(
                GroupORM.account_id == account_id, ContactGroupORM.contact_id == contact_id).all()
            return self._to_groups(groups)
        
    def get_all_contact_groups(self, account_id:int)->ContactGroups:
        with self.pool() as session:
            contactGroups = session.query(ContactGroupORM).filter(GroupORM.account_id == account_id).all()
            return self._to_contact_groups(contactGroups)

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

    def _to_contact_groups(self, contactGroups: List[ContactGroupORM])->ContactGroups:
        newContactGroups = ContactGroups()
        for contactGroup in contactGroups:
            newContactGroups.add(ContactGroup(contactGroup))
        return newContactGroups
