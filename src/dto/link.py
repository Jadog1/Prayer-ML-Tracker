from typing import List
import pandas as pd
from src.repo.orm import LinkORM

class Link():
    def __init__(self, link: LinkORM = None):
        if link:
            self.id = link.id
        
    def to_dict(self):
        return {
            'id': self.id
        }
    
    def from_dict(self, data: dict)->'Link':
        self.id = data.get('id')
        return self
    
class Links():
    def __init__(self):
        self.links: List[Link] = []

    def add(self, link: Link):
        self.links.append(link)
    
    def to_dataframe(self):
        rows = []
        for link in self.links:
            rows.append(link.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [link.to_dict() for link in self.links]