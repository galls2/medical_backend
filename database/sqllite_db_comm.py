# Imports
from database.i_db_comm import IDbComm
from pojos.event import Event
from pojos.force import Force
import sqlite3
import pprint

# Constants
DB_PATH = r".\medical_db.db"
GET_ALL_EVENTS_QUERY = "SELECT * FROM events"
GET_ALL_FORCES_QUERY = "SELECT * FROM forces"

def sql_query_db(query):
    try:
        records = None
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        print("Successfully Connected to SQLite")
        cur.execute(query)

        records = cur.fetchall()
        print("results are:", records)

        con.commit()
        print("SQLite table created")

        cur.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)

    finally:
        if con:
            con.close()
            print("sqlite connection is closed")

        return records


class SqlLiteDbComm(IDbComm):

    def __init__(self):
        x=0

    def get_all_events(self):
        records = sql_query_db(GET_ALL_EVENTS_QUERY)
        events_list = [Event(*rec) for rec in records]

        return events_list

    def get_all_forces(self):
        records = sql_query_db(GET_ALL_FORCES_QUERY)
        forces_list = [Force(*rec) for rec in records]

        return forces_list

    #def add_event


if __name__ == '__main__':
    sql_query_db('''''')
    # db_comm = SqlLiteDbComm()
    # events = db_comm.get_all_events()
