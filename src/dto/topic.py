from typing import List
import pandas as pd
from src.repo.orm import TopicORM

class Topic():
    def __init__(self, topic: TopicORM = None):
        if topic:
            self.id = topic.id
            self.name = topic.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def from_dict(self, data: dict)->'Topic':
        self.id = data.get('id')
        self.name = data.get('name')
        return self
    
class Topics():
    def __init__(self):
        self.topics: List[Topic] = []

    def add(self, topic: Topic):
        self.topics.append(topic)
    
    def to_dataframe(self):
        rows = []
        for topic in self.topics:
            rows.append(topic.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [topic.to_dict() for topic in self.topics]