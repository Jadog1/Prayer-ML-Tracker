from typing import List
import pandas as pd
from src.repo.orm import BibleTopicORM

class BibleTopic():
    def __init__(self, bibleTopic: BibleTopicORM = None, bibleType: str = None):
        if bibleTopic:
            self.id = bibleTopic.id
            self.book = bibleTopic.book
            self.chapter = bibleTopic.chapter
            self.verse_start = bibleTopic.verse_start
            self.verse_end = bibleTopic.verse_end
            self.text = bibleTopic.content
        self.type="section"
    
    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book,
            'chapter': self.chapter,
            'verse_start': self.verse_start,
            'verse_end': self.verse_end,
            'text': self.text
        }
    
    def from_dict(self, data: dict)->'BibleTopic':
        self.book = data.get('book')
        self.chapter = data.get('chapter')
        self.verse_start = data.get('verse_start')
        self.verse_end = data.get('verse_end')
        self.text = data.get('text')
        return self
    
class BibleTopics():
    def __init__(self):
        self.topics: List[BibleTopic] = []

    def add(self, topic: BibleTopic):
        self.topics.append(topic)
    
    def to_dataframe(self):
        rows = []
        for topic in self.topics:
            rows.append(topic.to_dict())
        
        return pd.DataFrame(rows)
    
    def to_list(self):
        return [topic.to_dict() for topic in self.topics]