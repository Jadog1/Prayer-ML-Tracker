from typing import List
import pandas as pd
from src.repo.orm import AccountORM

class Account():
    def __init__(self, account: AccountORM = None):
        self.id = account.id
        self.name = account.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
class Accounts():
    def __init__(self):
        self.accounts: List[Account] = []

    def add(self, account: Account):
        self.accounts.append(account)
    
    def to_dataframe(self):
        rows = []
        for account in self.accounts:
            rows.append(account.to_dict())
        
        return pd.DataFrame(rows)