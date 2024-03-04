from abc import ABC, abstractmethod
import pandas as pd
from ..data.prayerRequests import PrayerRequest, PrayerRequests
import psycopg2


class PrayerRequestRepo():
    def __init__(self, db: psycopg2.connection):
        self.db = db

    def get_subject(self, user_id:str, subject: str)->PrayerRequests:
        pass

    def get_daterange(self, user_id:str, start:str, end:str)->PrayerRequests:
        pass

    def save(self, user_id:str, prayerRequests: PrayerRequests, subject: str):
        pass