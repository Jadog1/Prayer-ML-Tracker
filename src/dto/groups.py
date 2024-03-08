from typing import List
import pandas as pd
from src.repo.orm import GroupORM

class Group():
    def __init__(self, group: GroupORM = None):
        if group:
            self.account_id = group.account_id
            self.name = group.name
            self.id = group.id
    
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'name': self.name,
            'id': self.id
        }
    
    def from_dict(self, data: dict)->'Group':
        self.account_id = data.get('account_id')
        self.name = data.get('name')
        self.id = data.get('id')
        return self
    
class Groups():
    def __init__(self):
        self.groups: List[Group] = []

    def add(self, group: Group):
        self.groups.append(group)
    
    def to_dataframe(self):
        rows = []
        for group in self.groups:
            rows.append(group.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [group.to_dict() for group in self.groups]