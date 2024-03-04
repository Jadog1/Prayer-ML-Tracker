import pandas as pd

class PrayerRequest():
    def __init__(self, subject: str, prayerRequest: str):
        self.subject = subject
        self.prayerRequest = prayerRequest
    
    def to_dict(self):
        return {"subject": self.subject, "prayerRequest": self.prayerRequest}

class PrayerRequests():
    def __init__(self):
        self.prayerRequests = []

    def add(self, prayer: PrayerRequest):
        self.prayerRequests.append(prayer)
    
    def to_dataframe(self):
        return pd.DataFrame(self.prayerRequests, columns=["subject", "prayerRequest"])