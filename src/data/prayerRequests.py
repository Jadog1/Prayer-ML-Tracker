import pandas as pd

class PrayerRequest():
    def __init__(self,  account_id: int, contact_id: int, prayer_request: str, archived_at: str):
        self.account_id = account_id
        self.contact_id = contact_id
        self.prayerRequest = prayer_request
        self.archived_at = archived_at
    
    def to_dict(self):
        return {
            "account_id": self.account_id,
            "contact_id": self.contact_id,
            "prayer_request": self.prayerRequest,
            "archived_at": self.archived_at
        }

class PrayerRequests():
    def __init__(self):
        self.prayerRequests = []

    def add(self, prayer: PrayerRequest):
        self.prayerRequests.append(prayer)
    
    def to_dataframe(self):
        rows = []
        for prayer in self.prayerRequests:
            rows.append(prayer.to_dict())
        return pd.DataFrame(rows, columns=["account_id", "contact_id", "prayer_request", "archived_at"])