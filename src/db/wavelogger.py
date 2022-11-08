import sys
from time import sleep
import sqlite3
import contextlib
from datetime import datetime


class wavelogger:

    __wavelog_filename = "wavelog.db"

    def __init__(self):
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS records(uid TEXT PRIMARY KEY DESC, dlt FLOAT, dlv INTEGER)")
                con.commit()

    '''
    Inserts an entry into the flat-file local database.
    
    entry: A tuple containing the 15 minute recorded results (UID, DLT, DLV)
        UID: A unique datetime object of when the recording took place (datetime.now())
        DLT: The delta of the largest trough/peak recorded in the 15 minute period
        DLV: True or False if the data was successfully delivered to the external database
    '''
    def insert(self, entry):
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("INSERT INTO records(uid, dlt, dlv) VALUES(?, ?, ?)", entry)
                con.commit()

    '''
    Selects an entry based off their datetime
    
    uid: The unique datetime object of the entry to search, i.e. uid
    Return: A tuple containing the values of the entry
    '''
    def select(self, uid):
        result = None
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("SELECT 'uid','dlt','dlv' FROM records WHERE uid = ?", (uid,))
                result = cur.fetchone()
        return result

    '''
    Deletes an entry based off their datetime.
    '''
    def delete(self, uid):
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("DELETE FROM records WHERE uid = ?", (uid,))
                pass

    '''
    Will update delivered status based off a datetime object.
    An example use can be to update the DELIVERED status of an entry that was recorded before 
    its attempted delivery (upon a successful response from a TCP socket).
    
    uid: The unique ID of an entry via datetime obj
    '''
    def set_delivered(self, uid):
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("UPDATE records SET dlv = 1 WHERE uid = ?", (uid,))
                con.commit()

    '''
    Selects all undelivered entries and returns an array sorted from least to most recently recorded.
    
    return: An array of all undelivered entries from oldest to newest recorded
    '''
    def select_all_undelivered(self):
        result = None
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("SELECT * FROM records WHERE dlv = 0")  # ORDER BY uid DESC
                result = cur.fetchall()
        return result

    '''
    Deletes all delivered entries
    
    '''
    def delete_all_delivered(self):
        with contextlib.closing(sqlite3.connect(self.__wavelog_filename)) as con:
            with contextlib.closing(con.cursor()) as cur:
                cur.execute("DELETE FROM records WHERE dlv = 1")
                con.commit()

    '''
    Allows for transition to another sqlite3.db file
    '''
    def change_database(self, dbfile):
        self.__wavelog_filename = dbfile


if __name__ == "__main__":
    idb = wavelogger()

    print(idb.select_all_undelivered())
