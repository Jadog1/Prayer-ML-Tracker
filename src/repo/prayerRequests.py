from abc import ABC, abstractmethod
import pandas as pd
from ..data.prayerRequests import PrayerRequest, PrayerRequests
import psycopg
import psycopg_pool
from psycopg.rows import dict_row, DictRow

class PrayerRequestRepo(ABC):
    @abstractmethod
    def get_all(self, account_id:int)->PrayerRequests:
        pass

    @abstractmethod
    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        pass

    @abstractmethod
    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        pass

    @abstractmethod
    def save(self, account_id:int, prayerRequests: PrayerRequests):
        pass

class PrayerRequestRepoImpl(PrayerRequestRepo):
    def __init__(self, pool: psycopg_pool.pool.ConnectionPool):
        self.pool = pool

    def get_all(self, account_id:int)->PrayerRequests:
        with self.pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            query = f"""
            SELECT {self._expected_select()}
            FROM prayer_request pr
            INNER JOIN account u ON pr.account_id = u.id
            INNER JOIN contact c on pr.contact_id = c.id
            WHERE pr.account_id = %s
            """
            cursor.execute(query, (account_id,))
            return self._fetch_expected_select(cursor)
        
    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        with self.pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            query = f"""
            SELECT {self._expected_select()}
            FROM prayer_request pr
            INNER JOIN account u ON pr.account_id = u.id
            INNER JOIN contact c on pr.contact_id = c.id
            WHERE pr.account_id = %s AND pr.contact_id = %s
            """
            cursor.execute(query, (account_id, contact_id))
            return self._fetch_expected_select(cursor)

    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        with self.pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            query = f"""
            SELECT {self._expected_select()}
            FROM prayer_request pr
            INNER JOIN account u ON pr.account_id = u.id
            INNER JOIN contact c on pr.contact_id = c.id
            WHERE pr.account_id = %s AND pr.created_at >= %s AND pr.created_at <= %s
            """
            cursor.execute(query, (account_id, start, end))
            return self._fetch_expected_select(cursor)
        
    def _expected_select(self):
        return "pr.account_id, pr.contact_id, pr.request, pr.archived_at"
    
    def _fetch_expected_select(self, cursor: psycopg.Cursor[DictRow])->PrayerRequests:
        requests = PrayerRequests()
        for row in cursor.fetchall():
            request = PrayerRequest(row["account_id"], row["contact_id"], row["request"], row["archived_at"])
            requests.add(request)
        return requests


    def save(self, account_id:int, prayerRequests: PrayerRequests):
        with self.pool.connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
            for request in prayerRequests.requests:
                query = """
                INSERT INTO prayer_request (account_id, contact_id, request, archived_at)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (account_id, request.contact_id, request.request, request.archived_at))

            return 


def OpenPGPool(uri: str)->psycopg_pool.pool.ConnectionPool:
    return psycopg_pool.pool.ConnectionPool(conninfo=uri)