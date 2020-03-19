# Imports
from database.i_db_comm import IDbComm
from pojos.event import Event
from pojos.force import Force

from pojos.event_type import EventType
from pojos.force_type import ForceType
import sqlite3
import pprint
import time

# Constants
DB_PATH = r".\medical_db.db"
ADD_EVENT_TYPE_QUERY = "INSERT INTO event_types (event_type_name) VALUES ('{}')"
ADD_FORCE_TYPE_QUERY = "INSERT INTO force_types (force_type_name) VALUES ('{}')"
GET_EVENT_TYPES_QUERY = "SELECT * FROM event_types"
GET_FORCE_TYPES_QUERY = "SELECT * FROM force_types"
GET_ALL_EVENTS_QUERY = '''SELECT event_id, timestamp, event_name, event_open, event_latitude, event_longitude, 
                          event_type_name, num_participants, event_description FROM events
                          LEFT JOIN event_types ON events.event_type_id = event_types.event_type_id'''
GET_ALL_FORCES_QUERY = '''SELECT force_id, force_name, force_latitude, force_longitude, force_type_name, event_name 
                          FROM forces
                          LEFT JOIN force_types ON forces.force_type_id = force_types.force_type_id
                          LEFT JOIN events ON forces.event_id = events.event_id'''
GET_ALL_OPEN_EVENTS_QUERY = '''SELECT event_id, timestamp, event_name, event_open, event_latitude, event_longitude, 
                          event_type_name, num_participants, event_description FROM events
                          LEFT JOIN event_types ON events.event_type_id = event_types.event_type_id
                          WHERE event_open = 1'''
ADD_EVENT_QUERY = '''INSERT INTO events (timestamp, event_name, event_latitude, event_longitude, event_type_id, 
num_participants, event_description)
VALUES ('{}', '{}', {}, {}, {}, {}, '{}')'''
ADD_FORCE_QUERY = '''INSERT INTO forces (force_name, force_latitude, force_longitude, force_type_id)
VALUES ('{}', {}, {}, {})'''
UPDATE_FORCE_POS_QUERY = '''UPDATE forces
SET force_latitude = {}, force_longitude = {}
WHERE force_id = {}'''
CLOSE_EVENT_QUERY = '''UPDATE events
SET event_open = 0
WHERE event_id = {}'''
CONNECT_FORCE_TO_EVENT_QUERY = '''UPDATE forces
SET event_id = {}
WHERE force_id = {}'''
FREE_FORCE_QUERY = '''UPDATE forces
SET event_id = -1
WHERE force_id = {}'''


def sql_query_db(query):
    try:
        records = None
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
    #    print("Successfully Connected to SQLite")
        cur.execute(query)

        records = cur.fetchall()
     #   print("results are:", records)

        con.commit()
      #  print("SQLite query executed successfully")

        cur.close()

    except sqlite3.Error as error:
        raise Exception("Error while creating a sqlite table", error)

    finally:
        if con:
            con.close()
       #     print("sqlite connection is closed")

        return records


class SqlLiteDbComm(IDbComm):
    def __init__(self):
        pass

    def add_event_type(self, event_type_name):
        sql_query_db(ADD_EVENT_TYPE_QUERY.format(event_type_name))

    def add_force_type(self, force_type_name):
        sql_query_db > (ADD_FORCE_TYPE_QUERY.format(force_type_name))

    def get_event_types(self):
        records = sql_query_db(GET_EVENT_TYPES_QUERY)
        events_type_list = [EventType(*rec) for rec in records]

        return events_type_list

    def get_force_types(self):
        records = sql_query_db(GET_FORCE_TYPES_QUERY)
        forces_type_list = [ForceType(*rec) for rec in records]

        return forces_type_list

    def get_all_events(self):
        records = sql_query_db(GET_ALL_EVENTS_QUERY)
        events_list = [Event(*rec) for rec in records]

        return events_list

    def get_all_forces(self):
        records = sql_query_db(GET_ALL_FORCES_QUERY)
        forces_list = [Force(*rec) for rec in records]

        return forces_list

    def add_event(self, timestamp, name, latitude, longitude, type_id, num_participants, description):
        sql_query_db(
            ADD_EVENT_QUERY.format(timestamp, name, latitude, longitude, type_id, num_participants, description))

    def add_force(self, name, latitude, longitude, type_id):
        sql_query_db(ADD_FORCE_QUERY.format(name, latitude, longitude, type_id))

    def get_all_open_events(self):
        records = sql_query_db(GET_ALL_OPEN_EVENTS_QUERY)
        events_list = [Event(*rec) for rec in records]

        return events_list

    def update_force_pos(self, force_id, latitude, longitude):
        sql_query_db(UPDATE_FORCE_POS_QUERY.format(latitude, longitude, force_id))

    def close_event(self, event_id):
        sql_query_db(CLOSE_EVENT_QUERY.format(event_id))

    def connect_force_to_event(self, force_id, event_id):
        sql_query_db(CONNECT_FORCE_TO_EVENT_QUERY.format(event_id, force_id))

    def free_force(self, force_id):
        sql_query_db(FREE_FORCE_QUERY.format(force_id))


if __name__ == '__main__':
    db_comm = SqlLiteDbComm()
    events = db_comm.get_all_open_events()
    pprint.pprint(events)
    # db_comm.update_force_pos(5, 32.0, 35.0)
    db_comm.connect_force_to_event(6, 1)
    # db_comm.free_force(6)
    forces = db_comm.get_all_forces()
    pprint.pprint(forces)

    event_types = db_comm.get_event_types()
    pprint.pprint(event_types)
    force_types = db_comm.get_force_types()
    pprint.pprint(force_types)
