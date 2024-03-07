import os
from repo.orm import OpenPool
from repo.contacts import ContactRepoImpl
from repo.prayerRequests import PrayerRequestRepoImpl

pg_uri = os.environ.get('PRAYERS_PG_DATABASE_URL')

class Repositories:
    def __init__(self, pg_uri):
        pool = OpenPool(pg_uri)
        self.prayer_request_repo = PrayerRequestRepoImpl(pool)
        self.contact_repo = ContactRepoImpl(pool)

repositories = Repositories(pg_uri)

def get_repositories():
    return repositories